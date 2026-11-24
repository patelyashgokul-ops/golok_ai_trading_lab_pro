import json
from datetime import datetime, timedelta, timezone

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from psycopg2.errors import LockNotAvailable

from ..services import market_data
from .sync import _ADMIN


MAX_TASKS = 60
MAX_FIXTURES = 512 * 1024
MODES = [("fixture", "Synthetic provider fixture"), ("live", "Authorized historical request")]
INTERVALS = [(key, key) for key, value in market_data.INTERVALS.items() if value]
RETRY = {"PROVIDER_BUSY", "RATE_LIMITED", "AUTH_REQUIRED", "DISCONNECTED", "DEGRADED",
         "LOCAL_AUTHORIZATION_REQUIRED", "LOCAL_CREDENTIALS_REQUIRED", "FRESH_AUTHORIZATION_REQUIRED"}


class SyncPlan(models.Model):
    _name = "golok.lab.sync.plan"
    _description = "Bounded historical synchronization plan"
    _order = "id desc"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    mode = fields.Selection(MODES, required=True, default="fixture")
    interval = fields.Selection(INTERVALS, required=True, default="5m")
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    mapping_ids = fields.Many2many("golok.lab.mapping", required=True, check_company=True)
    calendar_ids = fields.Many2many("golok.lab.calendar", required=True, check_company=True)
    fixture_input = fields.Text(groups="golok_ai_trading_lab_pro.group_admin")
    state = fields.Selection([("queued", "Queued"), ("done", "Finished"), ("partial", "Finished with failures"),
                              ("cancelled", "Cancelled")], required=True, default="queued")
    task_ids = fields.One2many("golok.lab.sync.task", "plan_id")

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group(_ADMIN):
            raise AccessError(_("Only a Trading System Administrator may submit a sync plan."))
        allowed = {"name", "mode", "interval", "starts", "ends", "mapping_ids", "calendar_ids", "fixture_input"}
        if len(vals_list) != 1 or set(vals_list[0]) - allowed:
            raise ValidationError(_("Submit only the plan inputs."))
        vals = dict(vals_list[0])
        raw = vals.pop("fixture_input", "") or ""
        if not isinstance(raw, str) or len(raw.encode()) > MAX_FIXTURES:
            raise ValidationError(_("Use at most 512 KiB of fixture input."))
        # Restrict relation commands to select operations to prevent side effects on the catalog.
        for key in ("mapping_ids", "calendar_ids"):
            commands = vals.get(key)
            if (not isinstance(commands, (list, tuple)) or not 1 <= len(commands) <= 8
                    or any(not isinstance(command, (tuple, list)) or len(command) != 3
                           or command[0] not in (fields.Command.LINK, fields.Command.SET)
                           or (command[0] == fields.Command.SET
                               and (not isinstance(command[2], (tuple, list)) or len(command[2]) > 8
                                    or any(type(item) is not int or item <= 0 for item in command[2])))
                           or (command[0] == fields.Command.LINK and (type(command[1]) is not int or command[1] <= 0))
                           for command in commands)):
                raise ValidationError(_("Select existing mapping and calendar records."))
        plan = super(SyncPlan, self.with_context({})).create([vals])
        plan._populate(raw)
        return plan

    def _populate(self, raw):
        self.ensure_one()
        company = self.env.company
        self.mapping_ids.check_access("read")
        self.calendar_ids.check_access("read")
        if (not 1 <= len(self.mapping_ids) <= 8 or not 1 <= len(self.calendar_ids) <= 2
                or any(record.company_id != company for record in self.mapping_ids)
                or any(record.company_id != company for record in self.calendar_ids)
                or not self.starts <= self.ends < self.starts + timedelta(days=31)
                or self.ends > fields.Date.today()):
            raise ValidationError(_("Select active-company inputs and up to 31 historical dates."))
        origin = "synthetic" if self.mode == "fixture" else "provider"
        verification = "fixture" if self.mode == "fixture" else "reviewed"
        revisions = {revision.exchange: (revision, revision._sessions()) for revision in self.calendar_ids}
        if len(revisions) != len(self.calendar_ids) or any(revision.verification != verification for revision in self.calendar_ids):
            raise ValidationError(_("Use one calendar per exchange with provenance matching the mode."))
        try:
            fixtures = json.loads(raw) if raw else {}
            if not isinstance(fixtures, dict) or len(fixtures) > MAX_TASKS or (fixtures and self.mode != "fixture"):
                raise ValueError
        except (ValueError, RecursionError):
            raise ValidationError(_("Fixture input must be an object keyed by mapping id and date.")) from None
        tasks, keys = [], set()
        as_of = datetime.now(timezone.utc)
        for offset in range((self.ends - self.starts).days + 1):
            day = self.starts + timedelta(days=offset)
            for mapping in self.mapping_ids.sorted("id"):
                if mapping.exchange not in revisions or mapping.provider != "smartapi" or not mapping._covers(day, origin):
                    raise ValidationError(_("Every selected mapping must cover the requested dates with compatible provenance."))
                revision, sessions = revisions[mapping.exchange]
                session = sessions.get(day)
                if not session or (session.closing and session.closing > as_of):
                    raise ValidationError(_("Every requested date needs an explicit closed or completed calendar session."))
                if session.kind == "closed":
                    continue
                key = f"{mapping.id}/{day.isoformat()}"
                keys.add(key)
                rows = fixtures.get(key)
                if self.mode == "fixture" and not isinstance(rows, list):
                    raise ValidationError(_("Supply fixture rows for every trading task using mapping_id/YYYY-MM-DD keys."))
                payload = json.dumps(rows, separators=(",", ":")) if rows is not None else False
                if payload and len(payload) > 256 * 1024:
                    raise ValidationError(_("A session fixture exceeds 256 KiB."))
                tasks.append({"company_id": company.id, "plan_id": self.id, "mapping_id": mapping.id,
                              "calendar_id": revision.id, "day": day, "interval": self.interval,
                              "mode": self.mode, "fixture_rows": payload})
                if len(tasks) > MAX_TASKS:
                    raise ValidationError(_("A plan allows at most 60 trading tasks."))
        if not tasks or fixtures.keys() - keys:
            raise ValidationError(_("A plan needs at least one task and fixture keys must match its trading sessions."))
        self.env["golok.lab.sync.task"].with_context({}).sudo().create(tasks)

    def _lock_plan(self):
        self.ensure_one()
        self.check_access("read")
        if not self.env.user.has_group(_ADMIN) or self.company_id != self.env.company:
            raise AccessError(_("Only an administrator of the active company may advance a plan."))
        try:
            with self.env.cr.savepoint():
                self.env.cr.execute("SELECT id FROM golok_lab_sync_plan WHERE id = %s FOR UPDATE NOWAIT", (self.id,))
        except LockNotAvailable:
            raise ValidationError(_("This plan is already being processed.")) from None
        self.invalidate_recordset()

    def action_process_next(self):
        self._lock_plan()
        if self.state != "queued":
            return
        task = self.task_ids.filtered(lambda item: item.state in ("queued", "retry"))[:1]
        if not task:
            return
        previous = self.env["golok.lab.sync"].search([
            ("company_id", "=", self.company_id.id), ("mapping_id", "=", task.mapping_id.id), ("day", "=", task.day),
            ("interval", "=", task.interval), ("mode", "=", task.mode), ("state", "=", "complete"),
            ("dataset_id.calendar_id", "=", task.calendar_id.id), ("dataset_id.quarantined", "=", False),
        ], limit=1)
        if previous and self.mode == "live":
            task.sudo().write({"report_id": previous.id, "state": "skipped", "fixture_rows": False})
        else:
            report = self.env["golok.lab.sync"]._run(task)
            attempts = task.attempts + 1
            state = ("done" if report.state == "complete" else
                     "retry" if report.reason in RETRY and attempts < 3 else "failed")
            task.sudo().write({"report_id": report.id, "attempts": attempts, "state": state,
                               **({"fixture_rows": False} if state != "retry" else {})})
        if not self.task_ids.filtered(lambda item: item.state in ("queued", "retry")):
            self.sudo().write({"state": "partial" if "failed" in self.task_ids.mapped("state") else "done"})

    def action_cancel(self):
        self._lock_plan()
        if self.state == "queued":
            self.task_ids.filtered(lambda item: item.state in ("queued", "retry")).sudo().write(
                {"state": "cancelled", "fixture_rows": False})
            self.sudo().write({"state": "cancelled"})


class SyncTask(models.Model):
    _name = "golok.lab.sync.task"
    _description = "Historical sync session checkpoint"
    _order = "day, id"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    plan_id = fields.Many2one("golok.lab.sync.plan", required=True, check_company=True, ondelete="cascade")
    mapping_id = fields.Many2one("golok.lab.mapping", required=True, check_company=True, ondelete="restrict")
    calendar_id = fields.Many2one("golok.lab.calendar", required=True, check_company=True, ondelete="restrict")
    mode = fields.Selection(MODES, required=True)
    interval = fields.Selection(INTERVALS, required=True)
    day = fields.Date(required=True)
    fixture_rows = fields.Text(groups="golok_ai_trading_lab_pro.group_admin")
    report_id = fields.Many2one("golok.lab.sync", check_company=True, ondelete="restrict")
    attempts = fields.Integer()
    state = fields.Selection([("queued", "Queued"), ("retry", "Retry available"), ("done", "Done"),
                              ("failed", "Failed"), ("skipped", "Already synchronized"),
                              ("cancelled", "Cancelled")], required=True, default="queued")
    _identity = models.Constraint("UNIQUE(plan_id,mapping_id,day)", "A session may occur once per plan.")

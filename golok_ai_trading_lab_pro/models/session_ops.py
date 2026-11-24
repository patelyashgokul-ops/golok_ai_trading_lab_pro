from datetime import timedelta, timezone

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Domain

from ..services import calendar, session_clock


PHASES = [(value, label) for value, label in (
    ("pre_market", "Pre-market"), ("market_opening", "Market opening"), ("intraday", "Intraday"),
    ("post_market", "Post-market"), ("closed", "Closed"), ("maintenance", "Maintenance"), ("blocked", "Blocked"))]


class SessionWatch(models.Model):
    _name = "golok.lab.session.watch"
    _description = "Fixture exchange research schedule"
    _rec_name = "dataset_id"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True, readonly=True)
    dataset_id = fields.Many2one("golok.lab.dataset", required=True, check_company=True, ondelete="restrict")
    active = fields.Boolean(default=True)
    checked_at = fields.Datetime(readonly=True)
    event_ids = fields.One2many("golok.lab.session.event", "watch_id")

    _dataset_watch = models.Constraint("UNIQUE(dataset_id)", "A dataset may have only one session watch.")

    @api.constrains("dataset_id")
    def _fixture_only(self):
        for watch in self:
            if watch.dataset_id.origin != "synthetic" or watch.dataset_id.calendar_id.verification != "fixture":
                raise ValidationError(_("This scheduler requires an explicit synthetic dataset and fixture calendar."))

    @api.model
    def _cron_dispatch(self):
        self.env["golok.lab.research.job"].sudo()._cron_run_durable()
        now = fields.Datetime.now().replace(tzinfo=timezone.utc)
        for watch in self.sudo().search([], order="checked_at asc nulls first, id", limit=32):
            watch.with_company(watch.company_id)._dispatch(now)

    def _dispatch(self, at):
        self.ensure_one()
        self.env.cr.execute("SELECT id FROM golok_lab_session_watch WHERE id=%s FOR UPDATE SKIP LOCKED", (self.id,))
        if not self.env.cr.fetchone():
            return self.env["golok.lab.session.event"]
        self.invalidate_recordset(["active", "dataset_id", "checked_at"])
        if not self.active:
            return self.env["golok.lab.session.event"]
        dataset = self.dataset_id
        day = at.astimezone(calendar.IST).date()
        sessions = dataset.calendar_id._sessions()
        previous_day = self.checked_at.replace(tzinfo=timezone.utc).astimezone(calendar.IST).date() if self.checked_at else day
        # Recover only explicit completed sessions, within the last seven calendar days.
        lower_bound = max(previous_day, day - timedelta(days=7))
        for missed_day in sorted(day_ for day_ in sessions if lower_bound <= day_ < day):
            missed = sessions[missed_day]
            if missed.kind != "closed" and missed.closing < at:
                self._record_phase(missed_day, missed, "post_market", at, recovery=True)
        self.sudo().write({"checked_at": at.replace(tzinfo=None)})
        session = sessions.get(day)
        phase = session_clock.phase(session, at)
        return self._record_phase(day, session, phase, at)

    def _record_phase(self, day, session, phase, at, *, recovery=False):
        dataset = self.dataset_id
        events = self.env["golok.lab.session.event"].sudo()
        domain = [("watch_id", "=", self.id), ("day", "=", day), ("phase", "=", phase)]
        known = events.search(domain, limit=1)
        if known:
            return known
        vals = {"watch_id": self.id, "company_id": self.company_id.id, "day": day, "phase": phase,
                "observed_at": at.replace(tzinfo=None), "mode": "fixture", "state": "completed",
                "summary": "NO TRADE · fixture research only", "recovered": recovery}
        if phase in ("market_opening", "intraday", "post_market"):
            cutoff = min(at, session.closing).replace(tzinfo=None)
            eligible = self.env["golok.lab.candle"].search_count(Domain([
                ("dataset_id", "=", dataset.id), ("available_at", "<=", cutoff),
                ("close_time", ">=", session.opening.replace(tzinfo=None))])
                & self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id"))
            vals["observation_count"] = eligible
            if eligible and not dataset.quarantined:
                try:
                    with self.env.cr.savepoint():
                        result = self.env["golok.lab.run"].create({"dataset_id": dataset.id, "as_of": cutoff})
                    vals["run_id"] = result.id
                except (AccessError, UserError):
                    vals.update(state="blocked", summary="NO TRADE · fixture research unavailable")
            else:
                vals.update(state="blocked", summary="NO TRADE · no permitted observations by cutoff")
        elif phase == "blocked" or dataset.quarantined:
            vals.update(state="blocked", summary="NO TRADE · calendar or data unavailable")
        if phase == "post_market":
            previous = events.search_count([("watch_id", "=", self.id), ("day", "=", day),
                                            ("phase", "in", ("pre_market", "market_opening", "intraday"))])
            vals["summary"] += f" · {previous} recorded earlier phases"
        if recovery:
            vals["summary"] += " · historical recovery"
        return events.create(vals)

    def action_check_now(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise AccessError(_("A schedule administrator in the active company is required."))
        record = self._dispatch(fields.Datetime.now().replace(tzinfo=timezone.utc))
        if not record:
            return False
        return {"type": "ir.actions.act_window", "res_model": record._name, "res_id": record.id,
                "views": [(False, "form")]}


class SessionEvent(models.Model):
    _name = "golok.lab.session.event"
    _description = "Exchange research phase report"
    _rec_name = "summary"
    _order = "day desc, observed_at desc, id desc"

    watch_id = fields.Many2one("golok.lab.session.watch", required=True, ondelete="restrict")
    company_id = fields.Many2one("res.company", required=True, index=True)
    day = fields.Date(required=True, index=True)
    phase = fields.Selection(PHASES, required=True)
    observed_at = fields.Datetime(required=True)
    mode = fields.Selection([("fixture", "Fixture-only research")], required=True)
    state = fields.Selection([("completed", "Completed"), ("blocked", "Blocked")], required=True)
    summary = fields.Char(required=True)
    observation_count = fields.Integer()
    recovered = fields.Boolean(readonly=True)
    run_id = fields.Many2one("golok.lab.run", ondelete="restrict")

    _phase_once = models.Constraint("UNIQUE(watch_id,day,phase)", "This phase has already been recorded.")

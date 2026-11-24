from datetime import timedelta
from time import perf_counter
from uuid import uuid4

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class ResearchJob(models.Model):
    _name = "golok.lab.research.job"
    _description = "Bounded historical research job"
    _rec_name = "dataset_id"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    dataset_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", check_company=True)
    requested_by = fields.Many2one("res.users", required=True, ondelete="restrict")
    cutoff = fields.Datetime(required=True)
    state = fields.Selection([("queued", "Queued"), ("claimed", "Claimed"), ("completed", "Completed"), ("failed", "Failed"),
                              ("cancelled", "Cancelled"), ("blocked", "Blocked by authorization")], required=True, index=True)
    finished_at = fields.Datetime()
    elapsed_ms = fields.Float()
    failure_reason = fields.Char()
    run_id = fields.Many2one("golok.lab.run", ondelete="restrict", check_company=True)
    attempts = fields.Integer(readonly=True)
    lease_until = fields.Datetime(readonly=True)
    worker_token = fields.Char(readonly=True)
    started_at = fields.Datetime(readonly=True)

    _identity = models.Constraint("UNIQUE(company_id,dataset_id,cutoff,requested_by)", "This research request already exists.")

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        if len(vals_list) != 1 or set(vals_list[0]) != {"dataset_id", "cutoff"}:
            raise ValidationError(_("Supply a dataset and one historical cutoff."))
        request = vals_list[0]
        dataset_id = request["dataset_id"]
        if type(dataset_id) is not int or dataset_id <= 0:
            raise ValidationError(_("Select one valid dataset."))
        try:
            cutoff = fields.Datetime.to_datetime(request["cutoff"])
        except (ValueError, TypeError):
            cutoff = None
        if not cutoff or cutoff.tzinfo or cutoff > fields.Datetime.now():
            raise ValidationError(_("Use a timezone-normalized historical cutoff."))
        company = self.env.company
        dataset = self.env["golok.lab.dataset"].search(
            [("id", "=", dataset_id), ("company_id", "=", company.id), ("quarantined", "=", False)], limit=1,
        )
        if not dataset:
            raise AccessError(_("Dataset unavailable."))
        dataset._permit("research")
        data = {"company_id": company.id, "dataset_id": dataset.id, "cutoff": cutoff, "requested_by": self.env.uid}
        prior = self.search([(key, "=", value) for key, value in data.items()], limit=1)
        if prior:
            return prior
        return super(ResearchJob, self.with_context({})).create([{**data, "state": "queued"}])

    def action_cancel(self):
        self.ensure_one()
        self.check_access("read")
        if self.requested_by != self.env.user or self.company_id != self.env.company:
            raise AccessError(_("Only the request owner may cancel this job."))
        self.env.cr.execute("SELECT state FROM golok_lab_research_job WHERE id=%s FOR UPDATE", [self.id])
        current = self.env.cr.fetchone()
        if current == ("cancelled",):
            self.invalidate_recordset(["state", "finished_at"])
            return True
        if current != ("queued",):
            raise UserError(_("Only queued jobs may be cancelled."))
        self.with_context({}).sudo().write({"state": "cancelled", "finished_at": fields.Datetime.now()})
        self.invalidate_recordset(["state", "finished_at"])
        return True

    def action_retry(self):
        self.ensure_one()
        self.check_access("read")
        if self.requested_by != self.env.user or self.company_id != self.env.company:
            raise AccessError(_("Only the request owner may retry this job."))
        self.env.cr.execute("SELECT state, attempts FROM golok_lab_research_job WHERE id=%s FOR UPDATE", (self.id,))
        state, attempts = self.env.cr.fetchone()
        if state == "queued":
            self.invalidate_recordset(["state", "finished_at", "failure_reason"])
            return True
        if state != "failed" or attempts >= 3:
            raise UserError(_("Only failed jobs with attempts remaining can be retried."))
        self.dataset_id._permit("research")
        self.with_context({}).sudo().write({"state": "queued", "finished_at": False, "failure_reason": False})
        self.invalidate_recordset(["state", "finished_at", "failure_reason"])
        return True

    @api.model
    def _cron_run_next(self):
        # One database-local job per invocation. A process interruption rolls back the claim and result.
        self.env.cr.execute("""
            SELECT id FROM golok_lab_research_job WHERE state='queued'
            ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1
        """)
        row = self.env.cr.fetchone()
        if not row:
            return
        self.browse(row[0])._complete_claim()

    @api.model
    def _claim_job(self, now):
        self.env.cr.execute("""
            SELECT id FROM golok_lab_research_job
            WHERE state='queued' OR (state='claimed' AND lease_until <= %s)
            ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1
        """, (now,))
        row = self.env.cr.fetchone()
        if not row:
            return self.browse()
        job = self.browse(row[0])
        if job.attempts >= 3:
            job.write({"state": "failed", "finished_at": now, "failure_reason": "Worker recovery attempts exhausted.",
                       "lease_until": False, "worker_token": False})
            return self.browse()
        job.write({"state": "claimed", "attempts": job.attempts + 1, "lease_until": now + timedelta(minutes=5),
                   "worker_token": uuid4().hex, "started_at": now})
        return job

    @api.model
    def _cron_run_durable(self):
        # The lease survives process exit. Result publication and the completed state share a transaction.
        with self.env.registry.cursor() as cursor:
            jobs = api.Environment(cursor, self.env.uid, {})[self._name].sudo()
            job = jobs._claim_job(fields.Datetime.now())
            identity = (job.id, job.worker_token) if job else None
            cursor.commit()
        if not identity:
            return
        with self.env.registry.cursor() as cursor:
            jobs = api.Environment(cursor, self.env.uid, {})[self._name].sudo()
            jobs._run_claim(*identity)
            cursor.commit()

    @api.model
    def _run_claim(self, identifier, token):
        self.env.cr.execute("""
            SELECT id FROM golok_lab_research_job
            WHERE id=%s AND worker_token=%s AND state='claimed' AND lease_until > %s
            FOR UPDATE SKIP LOCKED
        """, (identifier, token, fields.Datetime.now()))
        if self.env.cr.fetchone():
            self.browse(identifier)._complete_claim()

    def _complete_claim(self):
        self.ensure_one()
        started = perf_counter()
        vals = {}
        try:
            with self.env.cr.savepoint():
                requester = self.requested_by
                if not requester.active:
                    raise AccessError(_("Requester is inactive."))
                run = self.env["golok.lab.run"].with_user(requester).with_context(
                    {"allowed_company_ids": [self.company_id.id]}
                ).create({"dataset_id": self.dataset_id.id, "as_of": self.cutoff})
                vals.update(state="completed", run_id=run.id)
        except AccessError:
            vals.update(state="blocked", failure_reason="The request is no longer authorized.")
        except UserError:
            vals.update(state="failed", failure_reason="The request no longer meets research eligibility.")
        self.write({**vals, "finished_at": fields.Datetime.now(), "elapsed_ms": 1000 * (perf_counter() - started),
                    "worker_token": False, "lease_until": False})

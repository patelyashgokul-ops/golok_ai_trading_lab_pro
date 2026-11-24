from time import perf_counter

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
    state = fields.Selection([("queued", "Queued"), ("completed", "Completed"), ("failed", "Failed"),
                              ("cancelled", "Cancelled"), ("blocked", "Blocked by authorization")], required=True, index=True)
    finished_at = fields.Datetime()
    elapsed_ms = fields.Float()
    failure_reason = fields.Char()
    run_id = fields.Many2one("golok.lab.run", ondelete="restrict", check_company=True)

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
        if self.env.cr.fetchone() != ("queued",):
            raise UserError(_("Only queued jobs may be cancelled."))
        self.with_context({}).sudo().write({"state": "cancelled", "finished_at": fields.Datetime.now()})

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
        job = self.browse(row[0])
        started = perf_counter()
        vals = {}
        try:
            with self.env.cr.savepoint():
                requester = job.requested_by
                if not requester.active:
                    raise AccessError(_("Requester is inactive."))
                run = self.env["golok.lab.run"].with_user(requester).with_context(
                    {"allowed_company_ids": [job.company_id.id]}
                ).create({"dataset_id": job.dataset_id.id, "as_of": job.cutoff})
                vals.update(state="completed", run_id=run.id)
        except AccessError:
            vals.update(state="blocked", failure_reason="The request is no longer authorized.")
        except UserError:
            vals.update(state="failed", failure_reason="The request no longer meets research eligibility.")
        job.write({**vals, "finished_at": fields.Datetime.now(), "elapsed_ms": 1000 * (perf_counter() - started)})

import json
from time import perf_counter

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import research_v3


class ResearchFindings(models.Model):
    _name = "golok.lab.findings"
    _description = "Immutable supplemental historical research"
    _rec_name = "input_digest"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    run_id = fields.Many2one("golok.lab.run", required=True, ondelete="restrict", check_company=True)
    dataset_id = fields.Many2one(related="run_id.dataset_id")
    instrument_id = fields.Many2one(related="run_id.dataset_id.instrument_id")
    cutoff = fields.Datetime(related="run_id.as_of")
    input_digest = fields.Char(required=True)
    calculation_version = fields.Char(required=True)
    findings = fields.Text(required=True)
    elapsed_ms = fields.Float()

    _identity = models.Constraint("UNIQUE(run_id, calculation_version)", "Supplemental findings already exist.")

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        if len(vals_list) != 1 or set(vals_list[0]) != {"run_id"}:
            raise ValidationError(_("Supply one snapshot and no generated fields."))
        run_id = vals_list[0]["run_id"]
        if type(run_id) is not int or run_id <= 0:
            raise ValidationError(_("Select a valid snapshot."))
        company = self.env.company
        run = self.env["golok.lab.run"].search([("id", "=", run_id), ("company_id", "=", company.id)], limit=1)
        if not run:
            raise AccessError(_("Snapshot unavailable."))
        started = perf_counter()
        candles = run._checked_snapshot_candles()
        if not candles:
            raise ValidationError(_("No intact inputs for this snapshot."))
        identity = [("run_id", "=", run.id), ("calculation_version", "=", research_v3.VERSION)]
        prior = self.search(identity, limit=1)
        if prior:
            return prior
        warning = run.gap_count or any(item.get("quality_warning") for item in (run.evidence or {}).values())
        results = research_v3.analyze([row._to_bar() for row in reversed(candles)], warning)
        return super(ResearchFindings, self.with_context({})).create([{
            "company_id": company.id, "run_id": run.id, "input_digest": run.input_digest,
            "calculation_version": research_v3.VERSION, "findings": json.dumps(results, indent=2),
            "elapsed_ms": (perf_counter() - started) * 1000,
        }])


class ResearchRun(models.Model):
    _inherit = "golok.lab.run"

    def action_supplemental_findings(self):
        self.ensure_one()
        self.check_access("read")
        record = self.env["golok.lab.findings"].create({"run_id": self.id})
        return {"type": "ir.actions.act_window", "res_model": record._name,
                "res_id": record.id, "views": [(False, "form")], "target": "current"}

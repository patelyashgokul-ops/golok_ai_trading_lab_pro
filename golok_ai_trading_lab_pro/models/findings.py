import json
from decimal import Decimal
from time import perf_counter

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import eligibility, research_contract, research_v3


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
    evidence_contract = fields.Text(readonly=True)

    _identity = models.Constraint("UNIQUE(run_id, calculation_version)", "Supplemental findings already exist.")

    @api.model
    def _access_domain(self, operation):
        domain = super()._access_domain(operation)
        if operation == "read" and not self.env.su:
            domain &= self.env["golok.lab.holdout"]._observation_domain(
                "run_id.first_close", "run_id.last_close", "run_id.dataset_id.instrument_id")
        return domain

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        self.check_access("read")
        if any(row.dataset_id.origin != "synthetic" for row in self):
            raise AccessError(_("Historical market research is not exportable."))
        return super()._export_rows(fields, _is_toplevel_call=_is_toplevel_call)

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
        version = f"{research_v3.VERSION}/{research_contract.VERSION}"
        identity = [("run_id", "=", run.id), ("calculation_version", "=", version)]
        prior = self.search(identity, limit=1)
        if prior:
            return prior
        source_allowed = eligibility.evaluate(run.origin, "descriptive", quarantined=run.dataset_id.quarantined)[1]
        warning = not source_allowed or run.gap_count or any(item.get("quality_warning") for item in (run.evidence or {}).values())
        durations = {}
        results = research_v3.analyze([row._to_bar() for row in reversed(candles)], warning, durations=durations)
        contract = research_contract.snapshot({
            "instrument": run.dataset_id.instrument_id.id, "timeframe": run.dataset_id.interval,
            "research_timestamp": fields.Datetime.to_string(run.as_of), "dataset_fingerprint": run.input_digest,
            "input_freshness": "HISTORICAL_ONLY", "ohlcv_count": len(candles),
        }, run.evidence or {}, results, durations)
        return super(ResearchFindings, self.with_context({})).create([{
            "company_id": company.id, "run_id": run.id, "input_digest": run.input_digest,
            "calculation_version": version, "findings": json.dumps(results, indent=2),
            "evidence_contract": json.dumps(contract, indent=2),
            "elapsed_ms": (perf_counter() - started) * 1000,
        }])


class ResearchRun(models.Model):
    _inherit = "golok.lab.run"

    scanner_instrument_id = fields.Many2one(related="dataset_id.instrument_id", store=True, index=True)
    scanner_exchange = fields.Selection(related="dataset_id.instrument_id.exchange", store=True)
    scanner_interval = fields.Selection(related="dataset_id.interval", store=True)
    scanner_quarantined = fields.Boolean(related="dataset_id.quarantined")
    scanner_conflict = fields.Boolean(related="dataset_id.integrity_conflict")
    scanner_sector = fields.Char(related="dataset_id.mapping_id.sector")
    scanner_momentum = fields.Char(compute="_compute_scanner_metrics", string="ROC 10 (%)")
    scanner_relative_volume = fields.Char(compute="_compute_scanner_metrics", string="Relative Volume (20)")
    scanner_trend = fields.Char(compute="_compute_scanner_metrics", string="Trend Slope (20)")

    @api.depends("evidence")
    def _compute_scanner_metrics(self):
        for run in self:
            evidence = run.evidence or {}
            technical = evidence.get("RE-01") or {}
            volume = evidence.get("RE-05") or {}
            indicators = technical.get("indicators") or {}
            momentum = indicators.get("roc10")
            run.scanner_momentum = f"{Decimal(momentum) * 100:.4f}" if momentum is not None else False
            run.scanner_trend = indicators.get("trend_slope20")
            run.scanner_relative_volume = volume.get("finding") if volume.get("method") == "relative_volume20" else False

    @api.model
    def scanner_action(self):
        self.check_access("read")
        action = self.env["ir.actions.actions"]._for_xml_id("golok_ai_trading_lab_pro.action_stock_scanner")
        action["domain"] = [("company_id", "=", self.env.company.id)]
        return action

    @api.model
    def overview(self):
        data = super().overview()
        domain = [("company_id", "=", data["company_id"])]
        portfolio_domain = [*domain, *self._overview_cards()["portfolios"][1]]
        latest = self.env["golok.lab.portfolio"].search(portfolio_domain, limit=1)
        data["last_portfolio"] = False
        if latest:
            result = json.loads(latest.result)
            data["last_portfolio"] = {
                "id": latest.id, "strategy": latest.strategy, "ends": latest.ends,
                "initial_cash": result["initial_cash"], "ending_cash": result["ending_cash"],
                "gross": result["gross"], "fees": result["fees"], "net": result["net"],
                "suspended": latest.suspended, "trade_count": latest.trade_count,
            }
        return data

    def action_supplemental_findings(self):
        self.ensure_one()
        self.check_access("read")
        record = self.env["golok.lab.findings"].create({"run_id": self.id})
        return {"type": "ir.actions.act_window", "res_model": record._name,
                "res_id": record.id, "views": [(False, "form")], "target": "current"}

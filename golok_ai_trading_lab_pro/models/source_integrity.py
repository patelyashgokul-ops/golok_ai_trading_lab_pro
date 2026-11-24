import json
from datetime import timezone
from decimal import Decimal

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import calendar, price_integrity


class SourceComparison(models.Model):
    _name = "golok.lab.source.comparison"
    _description = "Equivalent source observation audit"
    _rec_name = "outcome"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    left_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", check_company=True)
    right_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", check_company=True)
    close_at = fields.Datetime(required=True)
    outcome = fields.Char(required=True, readonly=True)
    differences = fields.Text(readonly=True)
    upstreams = fields.Text(readonly=True)
    tolerance = fields.Char(readonly=True)

    _identity = models.Constraint("UNIQUE(left_id,right_id,close_at)", "This source pair and observation were already compared.")

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        self.check_access("read")
        if any(dataset.origin != "synthetic" for dataset in self.left_id | self.right_id):
            raise AccessError(_("Historical market comparison exports are disabled."))
        return super()._export_rows(fields, _is_toplevel_call=_is_toplevel_call)

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        if len(vals_list) != 1 or set(vals_list[0]) != {"left_id", "right_id", "close_at"}:
            raise ValidationError(_("Select two sources and a single closed observation."))
        vals = vals_list[0]
        inputs = (vals["left_id"], vals["right_id"])
        if any(type(value) is not int or value <= 0 for value in inputs) or inputs[0] == inputs[1]:
            raise ValidationError(_("Select two distinct datasets."))
        company = self.env.company
        datasets = self.env["golok.lab.dataset"].search([("id", "in", inputs), ("company_id", "=", company.id)], order="id")
        if len(datasets) != 2:
            raise AccessError(_("Both datasets must be in the active company."))
        left, right = datasets
        close_at = fields.Datetime.to_datetime(vals["close_at"])
        now = fields.Datetime.now().replace(tzinfo=timezone.utc)
        if not close_at or close_at.tzinfo or close_at > now.replace(tzinfo=None):
            raise ValidationError(_("Use a historical UTC observation closing time."))
        self.env["golok.lab.replay.guard"]._lock(datasets.instrument_id)
        identity = {"left_id": left.id, "right_id": right.id, "close_at": close_at}
        prior = self.search([(name, "=", value) for name, value in identity.items()], limit=1)
        if prior:
            return prior
        for dataset in datasets:
            dataset._permit("research")
        outcome, differences, upstreams, tolerance = self._compare_inputs(left, right, close_at, now)
        if outcome == "CONFLICT":
            datasets.sudo().write({"integrity_conflict": True})
        return super(SourceComparison, self.with_context({})).create([{
            **identity, "company_id": company.id, "outcome": outcome,
            "differences": json.dumps(differences, default=str), "upstreams": json.dumps(upstreams),
            "tolerance": str(tolerance),
        }])

    def _compare_inputs(self, left, right, close_at, now):
        if ((left.origin == "synthetic") != (right.origin == "synthetic") or left.instrument_id != right.instrument_id
                or left.interval != right.interval or not left.calendar_id or not right.calendar_id):
            return "NON_EQUIVALENT", {}, [], 0
        day = close_at.replace(tzinfo=timezone.utc).astimezone(calendar.IST).date()
        if any(not data.mapping_id or not data.mapping_id.isin or not data.mapping_id._covers(day, data.origin)
               for data in (left, right)):
            return "INSUFFICIENT_EVIDENCE", {}, [], 0
        pairs = []
        for data in (left, right):
            review = data.sudo().source_review_id
            if data.origin != "synthetic" and not review.raw_share_ohlcv:
                return "INSUFFICIENT_EVIDENCE", {}, [], 0
            row = self.env["golok.lab.candle"].search([("dataset_id", "=", data.id), ("close_time", "=", close_at)], limit=1)
            if not row or not row.available_at:
                return "INSUFFICIENT_EVIDENCE", {}, [], 0
            bar = row._to_bar()
            upstream = ("unknown" if data.origin == "synthetic" else
                        "NSE" if review.provider == "bhavcopy" else review.upstream or "unknown")
            observation = price_integrity.Observation(data.mapping_id.isin, data.instrument_id.exchange, "INR",
                                                       data.interval, "unadjusted", bar.close_time,
                                                       bar.available_at, bar.close, upstream)
            pairs.append((observation, bar))
        if pairs[0][1].open_time != pairs[1][1].open_time:
            return "NON_EQUIVALENT", {}, [], 0
        tolerance = max(Decimal(data.mapping_id.tick) for data in (left, right))
        outcome, differences = price_integrity.compare_bars(pairs[0][0], pairs[1][0], pairs[0][1], pairs[1][1], now, tolerance)
        return outcome, differences, [observation.upstream for observation, _ in pairs], tolerance

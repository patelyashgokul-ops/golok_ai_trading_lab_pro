import json
from datetime import timedelta, timezone
from decimal import Decimal
from urllib.parse import urlsplit

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import calendar, market_data, price_integrity


BROKER_SOURCES = frozenset({"smartapi", "upstox"})


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
    replacement_id = fields.Many2one("golok.lab.dataset", readonly=True, ondelete="restrict", check_company=True)
    resolution_reference = fields.Char(readonly=True)
    resolved_by = fields.Many2one("res.users", readonly=True, ondelete="restrict")
    resolved_at = fields.Datetime(readonly=True)

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
        return self._record_pair(left, right, close_at, now)

    @api.model
    def _source_key(self, dataset):
        if not dataset.mapping_id.isin or not dataset.calendar_id:
            return None
        if dataset.origin == "synthetic":
            # Only sealed acquisition paths take part in automatic synthetic quarantine.
            provider = dataset.mapping_id.provider
            if provider in BROKER_SOURCES and dataset.source.startswith(
                    ("SmartAPI fixture mapping ", "Upstox fixture mapping ")):
                return "fixture", provider
            return None
        review = dataset.sudo().source_review_id
        if not review.raw_share_ohlcv:
            return None
        if dataset.origin == "provider" and review.provider in BROKER_SOURCES:
            return "provider", review.provider
        if review.provider == "bhavcopy":
            return "daily_file", "NSE"
        if review.provider == "manual" and (dataset.replay_publication_digest or dataset.comparison_digest):
            return "publisher", review.upstream
        return None

    @api.model
    def _after_intake(self, dataset, bars):
        """Audit overlapping observations from distinct eligible intake sources."""
        source = self._source_key(dataset)
        if not source or not bars:
            return False
        domain = [
            ("id", "!=", dataset.id), ("company_id", "=", dataset.company_id.id),
            ("instrument_id", "=", dataset.instrument_id.id),
            ("interval", "=", dataset.interval),
            ("mapping_id.isin", "=", dataset.mapping_id.isin),
            ("quarantined", "=", False),
        ]
        if dataset.origin == "synthetic":
            domain += [("origin", "=", "synthetic"), ("mapping_id.provider", "in", sorted(BROKER_SOURCES)),
                       ("mapping_id.provider", "!=", dataset.mapping_id.provider)]
        else:
            domain += [("origin", "in", ("provider", "imported")),
                       "|", ("origin", "=", "provider"),
                       "|", ("source_review_id.provider", "=", "bhavcopy"),
                       "|", ("replay_publication_digest", "!=", False), ("comparison_digest", "!=", False)]
        candidates = self.env["golok.lab.dataset"].search([
            *domain, ("integrity_conflict", "=", False),
        ], order="id", limit=33)
        if len(candidates) == 33:
            raise ValidationError(_("Review duplicate source datasets before comparing this instrument."))
        peers = self.env["golok.lab.dataset"]
        for candidate in candidates:
            if (key := self._source_key(candidate)) and key != source:
                try:
                    candidate._permit("research")
                except AccessError:
                    continue
                peers |= candidate
        if not peers:
            return False
        if len(peers) > 8:
            raise ValidationError(_("Review duplicate source datasets before comparing this instrument."))
        try:
            dataset._permit("research")
        except AccessError:
            return False
        # This descriptive comparison uses already-stored rows. Daily receipt
        # metadata rounds upward by at most one minute for its CSV contract.
        now = fields.Datetime.now().replace(tzinfo=timezone.utc) + timedelta(seconds=60 if dataset.interval == "1d" else 1)
        closes = [bar.close_time.replace(tzinfo=None) for bar in bars]
        datasets = dataset | peers
        candles = self.env["golok.lab.candle"]
        observations = {(row.dataset_id.id, row.close_time): row._to_bar() for row in candles.search([
            ("dataset_id", "in", datasets.ids), ("close_time", "in", closes),
        ])}
        prior = self.sudo().search([
            ("company_id", "=", dataset.company_id.id), ("close_at", "in", closes),
            "|", "&", ("left_id", "=", dataset.id), ("right_id", "in", peers.ids),
            "&", ("left_id", "in", peers.ids), ("right_id", "=", dataset.id),
        ])
        compared = {(row.left_id.id, row.right_id.id, row.close_at) for row in prior}
        schedules = {revision.id: revision._sessions() for revision in datasets.calendar_id}
        new_audits = []
        conflicts = self.env["golok.lab.dataset"]
        for peer in peers:
            left, right = sorted((dataset, peer), key=lambda record: record.id)
            for close_at in closes:
                if ((left.id, close_at) not in observations or (right.id, close_at) not in observations
                        or (left.id, right.id, close_at) in compared):
                    continue
                values = self._comparison_values(left, right, close_at, now, observations=observations, schedules=schedules)
                new_audits.append(values)
                if values["outcome"] == "CONFLICT":
                    conflicts |= left | right
        if new_audits:
            super(SourceComparison, self.sudo().with_context({})).create(new_audits)
        if conflicts:
            conflicts.sudo().write({"integrity_conflict": True})
        return bool(conflicts)

    @api.model
    def _record_pair(self, left, right, close_at, now):
        identity = {"left_id": left.id, "right_id": right.id, "close_at": close_at}
        prior = self.search([(name, "=", value) for name, value in identity.items()], limit=1)
        if prior:
            return prior
        datasets = left | right
        for dataset in datasets:
            dataset._permit("research")
        values = self._comparison_values(left, right, close_at, now)
        if values["outcome"] == "CONFLICT":
            datasets.sudo().write({"integrity_conflict": True})
        return super(SourceComparison, self.with_context({})).create([values])

    def _comparison_values(self, left, right, close_at, now, *, observations=None, schedules=None):
        outcome, differences, upstreams, tolerance = self._compare_inputs(
            left, right, close_at, now, observations=observations, schedules=schedules)
        return {
            "left_id": left.id, "right_id": right.id, "close_at": close_at,
            "company_id": left.company_id.id, "outcome": outcome,
            "differences": json.dumps(differences, default=str), "upstreams": json.dumps(upstreams),
            "tolerance": str(tolerance),
        }

    def action_review_replacement(self):
        self.ensure_one()
        self._check_resolver()
        return {"type": "ir.actions.act_window", "res_model": "golok.lab.source.resolution",
                "target": "new", "views": [(False, "form")], "context": {"default_comparison_id": self.id}}

    def _check_resolver(self):
        self.check_access("read")
        if (self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin")):
            raise AccessError(_("An active-company source administrator is required."))
        if self.outcome != "CONFLICT" or self.replacement_id:
            raise ValidationError(_("Select an unresolved material conflict."))

    def _resolve(self, replacement, reference):
        self.ensure_one()
        self._check_resolver()
        replacement.check_access("read")
        self.env["golok.lab.replay.guard"]._lock(self.left_id.instrument_id)
        self.invalidate_recordset(["replacement_id"])
        self._check_resolver()
        try:
            parsed = urlsplit(reference or "")
            valid = (len(reference) <= 512 and parsed.scheme == "https" and parsed.hostname
                     and not parsed.username and not parsed.password and not parsed.query and not parsed.fragment)
        except (TypeError, ValueError):
            valid = False
        if not valid:
            raise ValidationError(_("Use an HTTPS correction reference without credentials or private query parameters."))
        originals = self.left_id | self.right_id
        if (not replacement or replacement in originals or replacement.company_id != self.company_id
                or replacement.instrument_id != self.left_id.instrument_id or replacement.interval != self.left_id.interval
                or replacement.mapping_id.isin != self.left_id.mapping_id.isin
                or (replacement.origin == "synthetic") != (self.left_id.origin == "synthetic")
                or not self._source_key(replacement)):
            raise ValidationError(_("Select a separate qualified replacement for the same instrument and interval."))
        replacement._permit("research")
        corroboration = self.search([
            ("company_id", "=", self.company_id.id), ("close_at", "=", self.close_at), ("outcome", "=", "MATCH"),
            "|", "&", ("left_id", "=", replacement.id), ("right_id", "not in", originals.ids),
            "&", ("right_id", "=", replacement.id), ("left_id", "not in", originals.ids),
        ])
        for support in corroboration:
            peer = (support.left_id | support.right_id) - replacement
            try:
                peer._permit("research")
            except AccessError:
                continue
            now = fields.Datetime.now()
            if (self._source_key(peer)
                    and self._compare_inputs(replacement, peer, self.close_at, now.replace(tzinfo=timezone.utc))[0] == "MATCH"):
                self.sudo().write({"replacement_id": replacement.id, "resolution_reference": reference,
                                   "resolved_by": self.env.uid, "resolved_at": now})
                return
        raise ValidationError(_("The replacement needs a current independent match for this observation."))

    def _compare_inputs(self, left, right, close_at, now, *, observations=None, schedules=None):
        if ((left.origin == "synthetic") != (right.origin == "synthetic") or left.instrument_id != right.instrument_id
                or left.interval != right.interval or not left.calendar_id or not right.calendar_id):
            return "NON_EQUIVALENT", {}, [], 0
        day = close_at.replace(tzinfo=timezone.utc).astimezone(calendar.IST).date()
        if any(not data.mapping_id or not data.mapping_id.isin or not data.mapping_id._covers(day, data.origin)
               for data in (left, right)):
            return "INSUFFICIENT_EVIDENCE", {}, [], 0
        pairs = []
        sessions = []
        for data in (left, right):
            review = data.sudo().source_review_id
            if data.origin != "synthetic" and not review.raw_share_ohlcv:
                return "INSUFFICIENT_EVIDENCE", {}, [], 0
            if observations is None:
                row = self.env["golok.lab.candle"].search([
                    ("dataset_id", "=", data.id), ("close_time", "=", close_at)], limit=1)
                bar = row._to_bar() if row else None
            else:
                bar = observations.get((data.id, close_at))
            if not bar or not bar.available_at:
                return "INSUFFICIENT_EVIDENCE", {}, [], 0
            try:
                schedule = schedules[data.calendar_id.id] if schedules is not None else data.calendar_id._sessions()
                sessions.append(calendar.validate_bar(bar, schedule, market_data.INTERVALS[data.interval]))
            except ValueError:
                return "NON_EQUIVALENT", {}, [], 0
            upstream = ("unknown" if data.origin == "synthetic" else
                        data.instrument_id.exchange if review.provider in ("bhavcopy", "upstox", "smartapi")
                        else review.upstream or "unknown")
            observation = price_integrity.Observation(data.mapping_id.isin, data.instrument_id.exchange, "INR",
                                                       data.interval, "unadjusted", bar.close_time,
                                                       bar.available_at, bar.close, upstream)
            pairs.append((observation, bar))
        if (pairs[0][1].open_time != pairs[1][1].open_time or sessions[0].kind != sessions[1].kind
                or sessions[0].windows() != sessions[1].windows()):
            return "NON_EQUIVALENT", {}, [], 0
        tolerance = max(Decimal(data.mapping_id.tick) for data in (left, right))
        outcome, differences = price_integrity.compare_bars(pairs[0][0], pairs[1][0], pairs[0][1], pairs[1][1], now, tolerance)
        if outcome == "CONFLICT":
            actions = self.env["golok.lab.corporate.action"].sudo().search([
                ("company_id", "=", left.company_id.id), ("instrument_id", "=", left.instrument_id.id),
                ("kind", "in", ("split", "bonus")), ("effective", ">=", day),
                ("effective", "<=", day + timedelta(days=30)), ("published_at", "<=", now.replace(tzinfo=None)),
            ], limit=16)
            for item in actions:
                low, high = sorted((pairs[0][1].close, pairs[1][1].close))
                larger, smaller = sorted((item.numerator, item.denominator), reverse=True)
                if larger > smaller and abs(low * larger - high * smaller) <= tolerance * smaller:
                    differences["possible_adjustment_action_id"] = item.id
                    break
        return outcome, differences, [observation.upstream for observation, _ in pairs], tolerance


class SourceResolution(models.TransientModel):
    _name = "golok.lab.source.resolution"
    _description = "Review a corroborated replacement"

    comparison_id = fields.Many2one("golok.lab.source.comparison", required=True, readonly=True)
    replacement_id = fields.Many2one("golok.lab.dataset", required=True)
    reference = fields.Char(required=True)

    def action_confirm(self):
        self.ensure_one()
        self.check_access("read")
        self.comparison_id._resolve(self.replacement_id, self.reference)
        return {"type": "ir.actions.act_window_close"}

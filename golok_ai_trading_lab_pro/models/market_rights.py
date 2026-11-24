import base64
import binascii
import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import bhavcopy, providers


PROVIDERS = [(key, source.name) for key, source in providers.SOURCES.items()]


class SourceReview(models.Model):
    _name = "golok.lab.source.review"
    _description = "Market data authorization review"
    _rec_name = "provider"
    _order = "id desc"

    company_id = fields.Many2one("res.company", required=True, index=True)
    provider = fields.Selection(PROVIDERS, required=True)
    terms_url = fields.Char(required=True)
    documentation = fields.Char(required=True)
    evidence = fields.Char(required=True)
    purpose = fields.Text(required=True)
    restrictions = fields.Text(required=True)
    expires = fields.Date(required=True)
    query = fields.Boolean()
    display = fields.Boolean()
    persist = fields.Boolean()
    automatic = fields.Boolean()
    backtest = fields.Boolean()
    optimize = fields.Boolean()
    fit = fields.Boolean()
    live = fields.Boolean()
    export = fields.Boolean()
    research = fields.Boolean(string="Descriptive research")
    upstream = fields.Char(help="Exact documented publisher identity for manual CSV.")
    revoked_at = fields.Datetime(readonly=True)
    retain_until = fields.Date(help="Optional date after which application access is blocked.")
    storage_policy = fields.Selection([("unknown", "Unverified"), ("archive", "Ongoing internal archival permitted")],
                                      default="unknown", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        allowed = {"provider", "terms_url", "documentation", "evidence", "purpose", "restrictions", "expires",
                   "storage_policy", "upstream", "retain_until", *providers.PERMISSIONS}
        if any(set(vals) - allowed for vals in vals_list):
            raise ValidationError(_("Supply only review evidence and explicit permissions."))
        for vals in vals_list:
            if vals.get("provider") == "manual" and not (vals.get("upstream") or "").strip():
                raise ValidationError(_("Record the exact upstream publisher for an authorized local file."))
            if vals.get("provider") != "fixture" and any(
                    not str(vals.get(key, "")).startswith("https://") or not urlsplit(str(vals[key])).hostname
                    for key in ("terms_url", "documentation")):
                raise ValidationError(_("Reference the official HTTPS terms and documentation."))
        results = self.browse()
        company = self.env.company.id
        for vals in vals_list:
            scope = [("company_id", "=", company), ("provider", "=", vals["provider"]), ("revoked_at", "=", False)]
            if vals["provider"] == "manual":
                scope.append(("upstream", "=", vals["upstream"]))
            self.sudo().search(scope).write({"revoked_at": fields.Datetime.now()})
            results += super(SourceReview, self.with_context({})).create([{**vals, "company_id": company}])
        return results

    @api.model
    def _authorize(self, source, feed, required, *, upstream=None, bound=None):
        domain = [("company_id", "=", self.env.company.id), ("provider", "=", source)]
        if source == "manual":
            if not upstream:
                raise AccessError(_("An exact upstream publisher is required."))
            domain.append(("upstream", "=", upstream))
        review = self.sudo().search(domain, limit=1)
        grants = {source: {name: review[name] for name in providers.PERMISSIONS}} if review else {}
        today = fields.Date.today()
        if (not review or (bound is not None and review.id != bound.id)
                or review.revoked_at or review.expires < today or (review.retain_until and review.retain_until < today)
                or ("persist" in required and review.storage_policy != "archive")
                or not providers.route([source], feed, required, grants)):
            raise AccessError(_("The bound source review must permit this operation and be current."))
        return review

    def action_revoke(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise AccessError(_("A source administrator of the active company is required."))
        if not self.revoked_at:
            self.sudo().write({"revoked_at": fields.Datetime.now()})


class DailyImport(models.Model):
    _name = "golok.lab.daily.import"
    _description = "Audited end-of-day Bhavcopy import"
    _order = "id desc"
    _rec_name = "digest"

    company_id = fields.Many2one("res.company", required=True, index=True)
    source = fields.Selection([("fixture", "Synthetic parser fixture"), ("bhavcopy", "Authorized NSE file")],
                              required=True)
    day = fields.Date(required=True)
    calendar_id = fields.Many2one("golok.lab.calendar", required=True, ondelete="restrict")
    review_id = fields.Many2one("golok.lab.source.review", required=True, ondelete="restrict")
    upload = fields.Binary(store=False, attachment=False)
    digest = fields.Char(required=True)
    accepted_key = fields.Char(index=True)
    status = fields.Selection([("accepted", "Accepted"), ("quarantine", "Quarantined")], required=True)
    count = fields.Integer()
    details = fields.Text(required=True)
    normalized_dataset_ids = fields.Many2many("golok.lab.dataset", readonly=True)
    _revision = models.Constraint("UNIQUE(company_id, source, day, calendar_id, digest)", "File revision already recorded.")
    _daily = models.Constraint("UNIQUE(company_id, accepted_key)", "An accepted daily revision already exists. Retry to compare it.")

    def export_data(self, fields_to_export):
        self.check_access("read")
        if any(row.source != "fixture" for row in self):
            raise AccessError(_("Historical market observations are not exportable."))
        return super().export_data(fields_to_export)

    def action_normalize(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise AccessError(_("A source administrator of the active company is required."))
        if self.status != "accepted":
            raise ValidationError(_("Only an accepted audit batch can be normalized."))
        review = self.env["golok.lab.source.review"]._authorize(
            self.source, "daily" if self.source == "bhavcopy" else "synthetic",
            ("query", "display", "persist"), bound=self.sudo().review_id)
        self.env.cr.execute("SELECT id FROM golok_lab_daily_import WHERE id=%s FOR UPDATE", (self.id,))
        self.invalidate_recordset(["normalized_dataset_ids"])
        datasets = self.normalized_dataset_ids
        if not datasets:
            datasets = self._normalize_rows(review)
            self.sudo().write({"normalized_dataset_ids": [fields.Command.set(datasets.ids)]})
        return {"type": "ir.actions.act_window", "name": _("Normalized daily datasets"),
                "res_model": datasets._name, "domain": [("id", "in", datasets.ids)],
                "views": [(False, "list"), (False, "form")]}

    def _normalize_rows(self, review):
        from ..services import market_data

        origin = "synthetic" if self.source == "fixture" else "imported"
        session = self.calendar_id._sessions()[self.day]
        if session.segments:
            raise ValidationError(_("Split sessions cannot be normalized to the current daily candle contract."))
        receipt = self.create_date.replace(tzinfo=timezone.utc)
        if receipt.second or receipt.microsecond:
            receipt = receipt.replace(second=0, microsecond=0) + timedelta(minutes=1)
        rows = {row["symbol"]: row for row in json.loads(self.details)}
        mappings = self.env["golok.lab.mapping"].search([
            ("company_id", "=", self.company_id.id), ("exchange", "=", "NSE"), ("provider", "=", "manual"),
            ("symbol", "in", list(rows)), ("starts", "<=", self.day), ("listing_status", "=", "listed"),
            ("verification", "=", "fixture" if origin == "synthetic" else "reviewed"),
            "|", ("ends", "=", False), ("ends", ">", self.day)], limit=65)
        if not 1 <= len(mappings) <= 64:
            raise ValidationError(_("Register 1–64 effective NSE mappings for authorized securities."))
        datasets = self.env["golok.lab.dataset"]
        for mapping in mappings:
            row = rows[mapping.symbol]
            if not mapping.isin or row["isin"] != mapping.isin:
                raise ValidationError(_("The source and the effective instrument mapping must agree on ISIN."))
            label = f"{self.source} / review {review.id} / calendar {self.calendar_id.id} / mapping {mapping.id}"
            dataset = self.env[datasets._name].search([
                ("company_id", "=", self.company_id.id), ("instrument_id", "=", mapping.instrument_id.id),
                ("source", "=", label), ("origin", "=", origin), ("interval", "=", "1d")], limit=1)
            if not dataset:
                dataset = datasets.sudo().create({
                    "name": label, "source": label, "origin": origin, "instrument_id": mapping.instrument_id.id,
                    "company_id": self.company_id.id, "calendar_id": self.calendar_id.id, "interval": "1d",
                    "source_review_id": review.id, "publication_basis": "receipt", "mapping_id": mapping.id,
                }).with_user(self.env.user)
            timestamp = lambda value: value.isoformat(timespec="seconds")
            bar = market_data.parse_bar(timestamp(session.closing), row["opening"], row["high"], row["low"], row["close"],
                                        str(row["volume"]), as_of=receipt, open_time=timestamp(session.opening),
                                        available_at=timestamp(receipt))
            dataset._import_bars([bar])
            datasets |= dataset
        return datasets

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        if len(vals_list) != 1 or set(vals_list[0]) != {"source", "day", "upload", "calendar_id"}:
            raise ValidationError(_("Supply source, trading date, calendar and one CSV or ZIP."))
        vals = vals_list[0]
        source = vals["source"]
        if source not in ("fixture", "bhavcopy"):
            raise ValidationError(_("Invalid file source."))
        review = self.env["golok.lab.source.review"]._authorize(
            source, "daily" if source == "bhavcopy" else "synthetic", ("query", "display", "persist"))
        day = fields.Date.to_date(vals["day"])
        calendar = self.env["golok.lab.calendar"].search([
            ("id", "=", vals["calendar_id"]), ("company_id", "=", self.env.company.id),
            ("exchange", "=", "NSE"), ("verification", "=", "fixture" if source == "fixture" else "reviewed")], limit=1)
        session = calendar._sessions().get(day) if calendar else None
        if not session or session.kind == "closed" or session.closing > datetime.now(timezone.utc):
            raise ValidationError(_("Select a matching completed NSE session."))
        data = vals["upload"]
        try:
            if not isinstance(data, (str, bytes)) or len(data) > 4 * ((bhavcopy.LIMIT + 2) // 3):
                raise ValueError
            raw = base64.b64decode(data, validate=True)
        except (ValueError, binascii.Error):
            raise ValidationError(_("Supply a bounded base64-encoded file.")) from None
        digest = hashlib.sha256(raw).hexdigest()
        key = {"company_id": self.env.company.id, "source": source, "day": day,
               "calendar_id": calendar.id, "digest": digest}
        prior = self.search([(field, "=", value) for field, value in key.items()], limit=1)
        if prior:
            return prior
        try:
            _, rows = bhavcopy.read(raw, day, today=fields.Date.today())
            accepted_key = f"{source}/{day}/{calendar.id}"
            existing = self.search([("company_id", "=", self.env.company.id), ("accepted_key", "=", accepted_key)], limit=1)
            details = json.dumps([asdict(rows[key]) for key in sorted(rows)], default=str)
            if existing:
                if existing.details == details:
                    return existing
                raise ValueError("Conflicting data for the same session.")
            report = {"status": "accepted", "count": len(rows),
                      "details": details, "accepted_key": accepted_key}
        except ValueError:
            report = {"status": "quarantine", "count": 0,
                      "details": "File rejected by date, schema, identity, OHLCV or archive validation."}
        return super(DailyImport, self.with_context({})).create([{**key, **report, "review_id": review.id}])

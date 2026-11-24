import base64
import binascii
import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
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
    storage_policy = fields.Selection([("unknown", "Unverified"), ("archive", "Ongoing internal archival permitted")],
                                      default="unknown", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        allowed = {"provider", "terms_url", "documentation", "evidence", "purpose", "restrictions", "expires",
                   "storage_policy", *providers.PERMISSIONS}
        if any(set(vals) - allowed for vals in vals_list):
            raise ValidationError(_("Supply only review evidence and explicit permissions."))
        for vals in vals_list:
            if vals.get("provider") != "fixture" and any(
                    not str(vals.get(key, "")).startswith("https://") or not urlsplit(str(vals[key])).hostname
                    for key in ("terms_url", "documentation")):
                raise ValidationError(_("Reference the official HTTPS terms and documentation."))
        return super(SourceReview, self.with_context({})).create([
            {**vals, "company_id": self.env.company.id} for vals in vals_list])

    @api.model
    def _authorize(self, source, feed, required):
        review = self.search([("company_id", "=", self.env.company.id), ("provider", "=", source)], limit=1)
        grants = {source: {name: review[name] for name in providers.PERMISSIONS}} if review else {}
        if (not review or review.expires < fields.Date.today()
                or ("persist" in required and review.storage_policy != "archive")
                or not providers.route([source], feed, required, grants)):
            raise AccessError(_("An effective review permitting file access, display and storage is required."))
        return review


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
    _revision = models.Constraint("UNIQUE(company_id, source, day, calendar_id, digest)", "File revision already recorded.")
    _daily = models.Constraint("UNIQUE(company_id, accepted_key)", "An accepted daily revision already exists. Retry to compare it.")

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

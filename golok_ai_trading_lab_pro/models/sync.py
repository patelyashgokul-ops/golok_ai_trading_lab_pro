import json
from dataclasses import replace
from datetime import datetime, timezone
from os import environ

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

from ..services import ingestion, market_data
from ..services.smartapi import ProviderError, SmartAPI
from . import provider

_ADMIN = "golok_ai_trading_lab_pro.group_admin"


class ProviderDataset(models.Model):
    _inherit = "golok.lab.dataset"

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su and any(
            vals.get("origin", self.env.context.get("default_origin")) == "provider"
            or str(vals.get("source", self.env.context.get("default_source", ""))).startswith(("SmartAPI fixture mapping ", "SmartAPI live mapping "))
            for vals in vals_list
        ):
            raise AccessError(_("Provider datasets must originate from the synchronization service."))
        return super().create(vals_list)


class Synchronization(models.Model):
    _name = "golok.lab.sync"
    _description = "Immutable historical synchronization attempt"
    _rec_name = "mapping_id"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    mapping_id = fields.Many2one("golok.lab.mapping", required=True, check_company=True, ondelete="restrict")
    dataset_id = fields.Many2one("golok.lab.dataset", check_company=True, ondelete="restrict")
    mode = fields.Selection([("fixture", "Synthetic provider fixture"), ("live", "Authorized historical request")], required=True)
    day = fields.Date(required=True)
    interval = fields.Selection([(key, key) for key in market_data.INTERVALS if key != "1d"], required=True)
    received_at = fields.Datetime()
    first_close = fields.Datetime()
    last_close = fields.Datetime()
    inserted = fields.Integer()
    count = fields.Integer()
    state = fields.Selection([("complete", "Complete"), ("rejected", "Rejected")], required=True)
    reason = fields.Char(required=True)

    @api.model
    def _client(self):
        if environ.get("GOLOK_SMARTAPI_AUTHORIZED") != "1":
            provider._SESSIONS.pop(self.env.cr.dbname, None)
            raise ProviderError("LOCAL_AUTHORIZATION_REQUIRED")
        if environ.get("GOLOK_SMARTAPI_HISTORY_OPEN_STAMPED") != "1":
            raise ProviderError("LOCAL_AUTHORIZATION_REQUIRED")
        return provider.cached_client(self.env.cr.dbname)

    @api.model
    def _fetch(self, wizard, session):
        if wizard.mode == "fixture":
            raw = json.loads(wizard.fixture_rows)
            client = SmartAPI(lambda *_: {"status": True, "data": raw})
            # Only the injected fixture transport sees this non-credential value.
            client._token = "fixture"
            return client.history(wizard.mapping_id.exchange, wizard.mapping_id.token, wizard.interval,
                                  session.opening, session.closing), client.last_success
        self.env["golok.lab.source.review"]._authorize("smartapi", "historical", ("query", "display", "persist"))
        if not provider._SESSION_LOCK.acquire(blocking=False):
            raise ProviderError("PROVIDER_BUSY")
        try:
            client = self._client()
            # Rebind quota to the current ORM request rather than retaining its cursor.
            client._quota = self.env["golok.lab.provider.budget"]._reserve
            try:
                if client._clock() < client._next_request:
                    raise ProviderError("RATE_LIMITED")
                return client.history(wizard.mapping_id.exchange, wizard.mapping_id.token, wizard.interval,
                                      session.opening, session.closing), client.last_success
            except ProviderError:
                if client.state == "AUTH_REQUIRED":
                    provider._SESSIONS.pop(self.env.cr.dbname, None)
                raise
            finally:
                client._quota = None
        finally:
            provider._SESSION_LOCK.release()

    @api.model
    def _run(self, wizard):
        company = self.env.company
        mapping, revision = wizard.mapping_id, wizard.calendar_id
        if mapping.company_id != company or revision.company_id != company:
            raise AccessError(_("Select available records in your active company."))
        base = {"company_id": company.id, "mapping_id": mapping.id, "mode": wizard.mode,
                "day": wizard.day, "interval": wizard.interval}
        report = {**base, "state": "rejected"}
        try:
            with self.env.cr.savepoint():
                origin = "synthetic" if wizard.mode == "fixture" else "provider"
                if mapping.provider != "smartapi" or not mapping._covers(wizard.day, origin):
                    raise ValidationError(_("The provider mapping is unavailable for that date and mode."))
                if revision.exchange != mapping.exchange or revision.verification != ("fixture" if origin == "synthetic" else "reviewed"):
                    raise ValidationError(_("The calendar exchange or provenance does not match the request."))
                seconds = market_data.INTERVALS[wizard.interval]
                session = revision._sessions().get(wizard.day)
                if not session or session.kind == "closed" or session.closing > datetime.now(timezone.utc):
                    raise ValidationError(_("Select a closed, covered trading session."))
                if wizard.mode == "fixture" and (not wizard.fixture_rows or len(wizard.fixture_rows) > 256 * 1024):
                    raise ValidationError(_("Supply bounded synthetic fixture rows."))
                rows, receipt = self._fetch(wizard, session)
                bars = ingestion.normalize(rows, session, seconds, receipt)
                source = f"SmartAPI {wizard.mode} mapping {mapping.id} calendar {revision.id}"
                datasets = self.env["golok.lab.dataset"]
                dataset = datasets.search([("company_id", "=", company.id), ("instrument_id", "=", mapping.instrument_id.id),
                                           ("interval", "=", wizard.interval), ("origin", "=", origin), ("source", "=", source)], limit=1)
                if not dataset:
                    dataset = datasets.with_context({}).sudo().create({
                        "name": source, "source": source, "origin": origin, "instrument_id": mapping.instrument_id.id,
                        "company_id": company.id, "calendar_id": revision.id, "mapping_id": mapping.id,
                        "interval": wizard.interval,
                    }).with_user(self.env.user)
                if dataset.mapping_id != mapping or dataset.calendar_id != revision:
                    raise ValidationError(_("The stored dataset has incompatible provenance."))
                existing = self.env["golok.lab.candle"].search([
                    ("dataset_id", "=", dataset.id), ("close_time", "in", [bar.close_time.replace(tzinfo=None) for bar in bars]),
                ])
                stored = [item._to_bar() for item in existing]
                first_availability = {bar.close_time: bar.available_at for bar in stored}
                bars = [replace(bar, available_at=first_availability.get(bar.close_time, bar.available_at)) for bar in bars]
                inserted = dataset._import_bars(bars)
                report.update(state="complete", dataset_id=dataset.id, received_at=receipt.replace(tzinfo=None),
                              first_close=bars[0].close_time.replace(tzinfo=None), last_close=bars[-1].close_time.replace(tzinfo=None),
                              inserted=inserted, count=len(bars), reason="Descriptive research only; historical publication is unverified.")
        except (ProviderError, ValidationError, ValueError, TypeError, RecursionError) as exc:
            safe_codes = {"LOCAL_AUTHORIZATION_REQUIRED", "LOCAL_CREDENTIALS_REQUIRED", "PROVIDER_BUSY", "RATE_LIMITED",
                          "AUTH_REQUIRED", "DISCONNECTED", "DEGRADED"}
            report["reason"] = (str(exc) if str(exc) in safe_codes else
                                "Synchronization rejected by authorization, schema, session or data integrity checks.")
        return self.with_context({}).sudo().create(report).with_user(self.env.user)


class SyncWizard(models.TransientModel):
    _name = "golok.lab.sync.wizard"
    _description = "Synchronize one closed historical session"

    mapping_id = fields.Many2one("golok.lab.mapping", required=True)
    calendar_id = fields.Many2one("golok.lab.calendar", required=True)
    day = fields.Date(required=True)
    interval = fields.Selection([(key, key) for key in market_data.INTERVALS if key != "1d"], required=True, default="5m")
    mode = fields.Selection([("fixture", "Synthetic fixture"), ("live", "Authorized SmartAPI historical")], required=True, default="fixture")
    fixture_rows = fields.Text()

    def action_sync(self):
        self.ensure_one()
        self.check_access("read")
        if not self.env.user.has_group(_ADMIN):
            raise AccessError(_("Only a Trading System Administrator may synchronize data."))
        self.mapping_id.check_access("read")
        self.calendar_id.check_access("read")
        result = self.env["golok.lab.sync"]._run(self)
        return {"type": "ir.actions.act_window", "res_model": result._name, "res_id": result.id,
                "views": [(False, "form")], "target": "current"}

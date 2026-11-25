"""Company-scoped Upstox configuration and bounded read-only collection."""

from datetime import timedelta, timezone
from os import environ

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import calendar, local_secrets, upstox, upstox_analytics
from ..services.smartapi import ProviderError
from .sync import _ADMIN


class AnalyticsConfig(models.Model):
    _name = "golok.lab.analytics.config"
    _description = "Private market data configuration"

    company_id = fields.Many2one("res.company", required=True, ondelete="cascade")
    operator_id = fields.Many2one("res.users", ondelete="set null")
    enabled = fields.Boolean()
    collect = fields.Boolean()
    backfill = fields.Boolean()
    schedule_research = fields.Boolean()
    mapping_id = fields.Many2one("golok.lab.mapping", ondelete="restrict")
    calendar_id = fields.Many2one("golok.lab.calendar", ondelete="restrict")
    envelope = fields.Text(copy=False)
    expires_at = fields.Datetime()
    connection = fields.Char(default="UNVERIFIED")
    historical = fields.Char(default="UNVERIFIED")
    instrument_master = fields.Char(default="UNVERIFIED")
    stream = fields.Char(default="UNVERIFIED")
    checked_at = fields.Datetime()
    observed_at = fields.Datetime()
    published_at = fields.Datetime()
    received_at = fields.Datetime()
    last_quote = fields.Char()
    next_collection = fields.Datetime()
    failures = fields.Integer()

    _company_once = models.Constraint("UNIQUE(company_id)", "One Analytics configuration per company.")

    def _admin(self):
        if not self.env.user.has_group(_ADMIN):
            raise AccessError(_("A Trading System Administrator is required."))

    @api.model
    def _current(self):
        return self.sudo().search([("company_id", "=", self.env.company.id)], limit=1)

    @api.model
    def _ensure_current(self):
        self._admin()
        company = self.env.company.id
        self.env.cr.execute("SELECT id FROM res_company WHERE id = %s FOR UPDATE", [company])
        return self._current() or self.sudo().with_context({}).create({"company_id": company})

    def _scope(self):
        return f"golok-upstox:v1:{self.env.cr.dbname}:{self.company_id.id}".encode()

    def _credential(self):
        if not self.enabled:
            raise ProviderError("LOCAL_AUTHORIZATION_REQUIRED")
        if not self.envelope or not self.expires_at or self.expires_at <= fields.Datetime.now():
            raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
        try:
            secret = local_secrets.open_secret(self.envelope, self._scope())
        except local_secrets.VaultError:
            raise ProviderError("LOCAL_CREDENTIALS_REQUIRED") from None
        if not upstox.credential_present(secret):
            raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
        return secret

    @api.model
    def _history_credential(self):
        settings = self._current()
        if settings:
            return settings._credential()
        # Preserve explicitly configured historical-only installations.
        if environ.get("GOLOK_UPSTOX_AUTHORIZED") == "1":
            return environ.get("GOLOK_UPSTOX_ANALYTICS_TOKEN")
        raise ProviderError("LOCAL_AUTHORIZATION_REQUIRED")

    @api.model
    def _store(self, secret, expires):
        self._admin()
        now = fields.Datetime.now()
        if not upstox.credential_present(secret) or not now < expires <= now + timedelta(days=366):
            raise ValidationError(_("Enter the complete token and its expiry from Upstox."))
        record = self._ensure_current()
        try:
            envelope = local_secrets.seal(secret, record._scope())
        except local_secrets.VaultError:
            raise ValidationError(_("The Windows Odoo worker could not open its local vault.")) from None
        record.write({"envelope": envelope, "expires_at": expires, "historical": "UNVERIFIED",
                      "connection": "UNVERIFIED", "stream": "UNVERIFIED", "last_quote": False,
                      "observed_at": False, "published_at": False, "received_at": False,
                      "next_collection": False, "failures": 0})
        self._probe(record)
        return self._public_status(record)

    @api.model
    def _public_status(self, record):
        return {"stored": bool(record.envelope), "expires_at": fields.Datetime.to_string(record.expires_at),
                "connection": record.connection or "UNVERIFIED"}

    def _mapping(self, record, day):
        mapping = record.mapping_id
        if (not mapping or mapping.provider != "upstox" or mapping.company_id != self.env.company
                or not mapping._covers(day, "provider") or not upstox.identity(mapping.exchange, mapping.token, mapping.isin)):
            raise ProviderError("REVIEWED_MAPPING_REQUIRED")
        return mapping

    def _probe(self, record):
        state = "DISABLED"
        if record.enabled:
            try:
                token = record._credential()
                self.env["golok.lab.source.review"]._authorize("upstox", "historical", "query")
                mapping = self._mapping(record, calendar_day())
                upstox_analytics.quote_snapshot(token, mapping.token, mapping.isin, self.env["golok.lab.provider.budget"]._reserve)
                state = "READ_ONLY_QUOTE_VERIFIED"
            except AccessError:
                state = "PERMISSION_REQUIRED"
            except ProviderError as exc:
                state = str(exc)
        record.write({"connection": state, "checked_at": fields.Datetime.now()})

    @api.model
    def _cron_collect(self):
        now = fields.Datetime.now()
        configs = self.sudo()
        for record in configs.search([("enabled", "=", True), "|", ("collect", "=", True), ("backfill", "=", True)],
                                     order="id", limit=20):
            with self.env.cr.savepoint():
                self.env.cr.execute("SELECT id FROM golok_lab_analytics_config WHERE id = %s FOR UPDATE SKIP LOCKED", [record.id])
                if not self.env.cr.fetchone():
                    continue
                record.invalidate_recordset()
                operator = record.operator_id
                if not operator.active or record.company_id not in operator.company_ids or not operator.has_group(_ADMIN):
                    continue
                service = self.with_user(operator).with_context(allowed_company_ids=[record.company_id.id])
                if record.backfill:
                    service._backfill(record)
                if record.collect and (not record.next_collection or record.next_collection <= now):
                    service._collect(record, now)

    def _collect(self, record, now):
        try:
            token = record._credential()
            self.env["golok.lab.source.review"]._authorize("upstox", "historical", "analytics_collect")
            day = calendar_day(now)
            mapping = self._mapping(record, day)
            revision = record.calendar_id
            session = revision._sessions().get(day) if revision.verification == "reviewed" else None
            at = now.replace(tzinfo=timezone.utc)
            if not session or session.kind != "regular" or not session.opening <= at < session.closing:
                raise ProviderError("OUTSIDE_REVIEWED_SESSION")
            self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [day], self.env.company)
            sample = upstox_analytics.stream_sample(token, mapping.token, mapping.isin,
                                                     self.env["golok.lab.provider.budget"]._reserve)
            if not sample or not session.opening <= sample["event"] <= sample["published"] < session.closing:
                raise ProviderError("STALE_OR_UNAVAILABLE")
        except (AccessError, ValidationError):
            self._stream_failure(record, now, "PERMISSION_OR_HOLDOUT_BLOCKED")
        except ProviderError as exc:
            self._stream_failure(record, now, str(exc))
        else:
            times = {f"{name}_at": sample[key].replace(tzinfo=None) for name, key in
                     (("observed", "event"), ("published", "published"), ("received", "receipt"))}
            record.write({**times, "last_quote": sample["price"], "stream": "FRESH_SAMPLE",
                          "failures": 0, "next_collection": now + timedelta(seconds=60)})

    def _stream_failure(self, record, now, status):
        failures = min(6, record.failures + 1)
        record.write({"failures": failures, "stream": status, "last_quote": False, "observed_at": False,
                      "published_at": False, "received_at": False,
                      "next_collection": now + timedelta(seconds=min(900, 30 * 2**failures))})

    def _backfill(self, record):
        try:
            record._credential()
            self.env["golok.lab.source.review"]._authorize("upstox", "historical", "analytics_backfill")
        except (ProviderError, AccessError):
            record.write({"historical": "BACKFILL_BLOCKED"})
            return
        plans = self.env["golok.lab.sync.plan"]
        plan = plans.search([("company_id", "=", self.env.company.id), ("mode", "=", "live"),
                             ("state", "=", "queued"), ("mapping_ids", "=", record.mapping_id.id)],
                            order="id", limit=1)
        if not plan or set(plan.mapping_ids.ids) != {record.mapping_id.id} or plan.calendar_ids.ids != record.calendar_id.ids:
            return
        try:
            with self.env.cr.savepoint():
                plan.action_process_next()
        except (AccessError, ValidationError):
            record.write({"historical": "BACKFILL_BLOCKED"})
            return
        task = plan.task_ids.filtered(lambda row: row.report_id and row.state == "done").sorted("id")[-1:]
        if task:
            report = task.report_id
            record.write({"historical": "CLOSED_SESSION_GRID_VERIFIED"})
            if record.schedule_research:
                try:
                    with self.env.cr.savepoint():
                        self.env["golok.lab.research.job"].create({
                            "dataset_id": report.dataset_id.id, "cutoff": report.received_at,
                        })
                except (AccessError, ValidationError):
                    record.write({"historical": "GRID_VERIFIED_RESEARCH_BLOCKED"})


def calendar_day(now=None):
    now = now or fields.Datetime.now()
    return now.replace(tzinfo=timezone.utc).astimezone(calendar.IST).date()


class AnalyticsWorkspace(models.TransientModel):
    _name = "golok.lab.analytics.workspace"
    _description = "Market Data API Configuration"

    provider = fields.Selection([("offline", "Offline"), ("upstox", "Upstox Analytics")], required=True)
    mapping_id = fields.Many2one("golok.lab.mapping")
    calendar_id = fields.Many2one("golok.lab.calendar")
    collect = fields.Boolean(string="Collect timestamped V3 samples")
    backfill = fields.Boolean(string="Automatically advance permitted historical plans")
    schedule_research = fields.Boolean(string="Queue descriptive research after backfill")
    credential_state = fields.Char(readonly=True)
    connection = fields.Char(readonly=True)
    historical = fields.Char(readonly=True)
    stream = fields.Char(readonly=True)
    instrument_master = fields.Char(readonly=True)

    @api.model
    def default_get(self, names):
        values = super().default_get(names)
        service = self.env["golok.lab.analytics.config"]
        service._admin()
        config = service._current()
        values.update({field: value for field, value in {
            "provider": "upstox" if config.enabled else "offline",
            "mapping_id": config.mapping_id.id, "calendar_id": config.calendar_id.id,
            "backfill": config.backfill, "collect": config.collect, "schedule_research": config.schedule_research,
            "connection": config.connection or "UNVERIFIED", "historical": config.historical or "UNVERIFIED",
            "stream": config.stream or "UNVERIFIED", "instrument_master": config.instrument_master or "UNVERIFIED",
            "credential_state": fields.Datetime.to_string(config.expires_at) if config.envelope else "NOT STORED",
        }.items() if field in names})
        return values

    def _service(self):
        self.ensure_one()
        self.check_access("read")
        service = self.env["golok.lab.analytics.config"]
        service._admin()
        return service

    def _reload(self):
        return self.env["ir.actions.actions"]._for_xml_id("golok_ai_trading_lab_pro.action_analytics_workspace")

    def action_apply(self):
        service = self._service()
        enabled = self.provider == "upstox"
        if enabled and (self.mapping_id.company_id != self.env.company or self.mapping_id.provider != "upstox"
                        or self.mapping_id.verification != "reviewed"):
            raise ValidationError(_("Choose a reviewed Upstox mapping in the active company."))
        if enabled and (self.collect or self.backfill) and (
                self.calendar_id.company_id != self.env.company or self.calendar_id.verification != "reviewed"
                or self.calendar_id.exchange != "NSE"):
            raise ValidationError(_("Choose a reviewed company NSE calendar for automation."))
        record = service._ensure_current()
        record.write({"enabled": enabled, "operator_id": self.env.uid, "mapping_id": self.mapping_id.id if enabled else False,
                      "calendar_id": self.calendar_id.id if enabled else False, "collect": enabled and self.collect,
                      "backfill": enabled and self.backfill, "schedule_research": enabled and self.schedule_research,
                      "next_collection": False, "failures": 0, "stream": "UNVERIFIED", "last_quote": False,
                      "observed_at": False, "published_at": False, "received_at": False})
        return self._reload()

    def action_test_connection(self):
        service = self._service()
        service._probe(service._ensure_current())
        return self._reload()

    def action_check_master(self):
        service = self._service()
        record = service._ensure_current()
        try:
            record._credential()
            self.env["golok.lab.source.review"]._authorize("upstox", "historical", "query")
            mapping = service._mapping(record, calendar_day())
            instrument = upstox_analytics.instrument_master(self.env["golok.lab.provider.budget"]._reserve).get(mapping.token)
            status = ("MASTER_MATCH" if instrument and instrument["isin"] == mapping.isin
                      and instrument["symbol"] == mapping.symbol and instrument["lot"] == mapping.lot else "REVIEW_MAPPING_MISMATCH")
        except AccessError:
            status = "PERMISSION_REQUIRED"
        except ProviderError as exc:
            status = str(exc)
        record.write({"instrument_master": status})
        return self._reload()

    def action_manage_token(self):
        self._service()
        return {"type": "ir.actions.client", "tag": "golok_lab.analytics_secret",
                "name": _("Upstox Analytics Credential"), "params": {"company_id": self.env.company.id}}

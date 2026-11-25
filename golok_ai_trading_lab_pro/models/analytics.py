"""Company-scoped Upstox configuration and bounded read-only collection."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from os import environ

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Domain

from ..services import calendar, ingestion, local_secrets, upstox, upstox_analytics
from ..services.smartapi import ProviderError
from .sync import _ADMIN


class AnalyticsConfig(models.Model):
    _name = "golok.lab.analytics.config"
    _description = "Private market data configuration"

    company_id = fields.Many2one("res.company", required=True, ondelete="cascade")
    operator_id = fields.Many2one("res.users", ondelete="set null")
    enabled = fields.Boolean()
    collect = fields.Boolean()
    worker_capture = fields.Boolean()
    backfill = fields.Boolean()
    schedule_research = fields.Boolean()
    mapping_id = fields.Many2one("golok.lab.mapping", ondelete="restrict")
    calendar_id = fields.Many2one("golok.lab.calendar", ondelete="restrict")
    envelope = fields.Text(copy=False)
    expires_at = fields.Datetime()
    connection = fields.Char(default="UNVERIFIED")
    historical = fields.Char(default="UNVERIFIED")
    instrument_master = fields.Char(default="UNVERIFIED")
    reference_checked_at = fields.Datetime()
    reference_symbol = fields.Char()
    reference_isin = fields.Char()
    stream = fields.Char(default="UNVERIFIED")
    checked_at = fields.Datetime()
    observed_at = fields.Datetime()
    published_at = fields.Datetime()
    received_at = fields.Datetime()
    last_quote = fields.Char()
    sample_review_id = fields.Many2one("golok.lab.source.review", ondelete="set null")
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
                reviews = self.env["golok.lab.source.review"]
                reserve = self.env["golok.lab.provider.budget"]._reserve
                try:
                    reviews._authorize("upstox", "historical", "analytics_quote")
                except AccessError:
                    reviews._authorize("upstox", "historical", "query")
                    self._probe_history(record, token, reserve)
                    state = "READ_ONLY_HISTORY_VERIFIED"
                else:
                    mapping = self._mapping(record, calendar_day())
                    upstox_analytics.quote_snapshot(token, mapping.token, mapping.isin, reserve)
                    state = "READ_ONLY_QUOTE_VERIFIED"
            except AccessError:
                state = "PERMISSION_REQUIRED"
            except ProviderError as exc:
                state = str(exc)
        record.write({"connection": state, "checked_at": fields.Datetime.now()})

    def _probe_history(self, record, token, reserve):
        revision = record.calendar_id
        if revision.verification != "reviewed" or revision.company_id != self.env.company or revision.exchange != "NSE":
            raise ProviderError("REVIEWED_CALENDAR_REQUIRED")
        now = fields.Datetime.now().replace(tzinfo=timezone.utc)
        eligible = [session for session in revision._sessions().values()
                    if session.kind == "regular" and session.closing <= now and record.mapping_id._covers(session.day, "provider")]
        if not eligible:
            raise ProviderError("CLOSED_SESSION_REQUIRED")
        session = max(eligible, key=lambda item: item.day)
        mapping = self._mapping(record, session.day)
        self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [session.day], self.env.company)
        rows, received = upstox.history(token, mapping.token, mapping.isin, "5m", session, reserve)
        try:
            ingestion.normalize(rows, session, 300, received)
        except ValueError:
            raise ProviderError("DEGRADED") from None
        record.write({"historical": "CLOSED_SESSION_GRID_VERIFIED"})

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
                if record.collect and not record.worker_capture and (not record.next_collection or record.next_collection <= now):
                    service._collect(record, now)

    def _stream_scope(self, record, now):
        review = self.env["golok.lab.source.review"]._authorize("upstox", "historical", "analytics_collect")
        day = calendar_day(now)
        mapping = self._mapping(record, day)
        revision = record.calendar_id
        session = (revision._sessions().get(day)
                   if revision.verification == "reviewed" and revision.company_id == self.env.company else None)
        at = now.replace(tzinfo=timezone.utc)
        if not session or session.kind != "regular" or not session.opening <= at < session.closing:
            raise ProviderError("OUTSIDE_REVIEWED_SESSION")
        self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [day], self.env.company)
        return review, mapping, session

    def _collect(self, record, now):
        try:
            token = record._credential()
            review, mapping, session = self._stream_scope(record, now)
            sample = upstox_analytics.stream_sample(token, mapping.token, mapping.isin,
                                                     self.env["golok.lab.provider.budget"]._reserve)
            if not sample or not session.opening <= sample["event"] <= sample["published"] < session.closing:
                raise ProviderError("STALE_OR_UNAVAILABLE")
            self.env["golok.lab.replay.guard"]._lock(mapping.instrument_id)
            self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [session.day], self.env.company)
        except (AccessError, ValidationError):
            self._stream_failure(record, now, "PERMISSION_OR_HOLDOUT_BLOCKED")
        except ProviderError as exc:
            self._stream_failure(record, now, str(exc))
        else:
            self._update_latest(record, review, sample, now + timedelta(seconds=60))

    def _update_latest(self, record, review, sample, next_collection=False):
        times = {f"{name}_at": sample[key].replace(tzinfo=None) for name, key in
                 (("observed", "event"), ("published", "published"), ("received", "receipt"))}
        record.write({**times, "last_quote": sample["price"], "stream": "FRESH_SAMPLE",
                      "sample_review_id": review.id, "failures": 0, "next_collection": next_collection})

    def _store_worker_sample(self, record, review, mapping, session, sample):
        now = fields.Datetime.now().replace(tzinfo=timezone.utc)
        if (not session.opening <= sample["event"] <= sample["published"] < session.closing
                or not sample["published"] <= sample["receipt"] <= now + timedelta(seconds=1)
                or now - sample["event"] > upstox_analytics.MAX_AGE):
            return
        self.env["golok.lab.replay.guard"]._lock(mapping.instrument_id)
        self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [session.day], self.env.company)
        self.env["golok.lab.analytics.tick"]._append(mapping, review, sample)
        if not record.observed_at or record.observed_at <= sample["event"].replace(tzinfo=None):
            self._update_latest(record, review, sample)

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


class AnalyticsTick(models.Model):
    _name = "golok.lab.analytics.tick"
    _description = "Private timestamped Upstox LTPC observation"
    _log_access = False

    company_id = fields.Many2one("res.company", required=True, index=True, ondelete="cascade")
    mapping_id = fields.Many2one("golok.lab.mapping", required=True, index=True, ondelete="restrict")
    review_id = fields.Many2one("golok.lab.source.review", required=True, ondelete="restrict")
    event_ms = fields.Char(required=True)
    publication_ms = fields.Char(required=True)
    received_at = fields.Datetime(required=True)
    price = fields.Char(required=True)

    _once = models.Constraint("UNIQUE(mapping_id, review_id, event_ms, price)", "This LTPC observation already exists.")

    @api.model
    def _append(self, mapping, review, sample):
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        utc_times = {key: str((sample[key] - epoch) // timedelta(milliseconds=1)) for key in ("event", "published")}
        self.env.cr.execute("""
            INSERT INTO golok_lab_analytics_tick
                (company_id, mapping_id, review_id, event_ms, publication_ms, received_at, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (mapping_id, review_id, event_ms, price) DO NOTHING
            """, [mapping.company_id.id, mapping.id, review.id, utc_times["event"], utc_times["published"],
                  sample["receipt"].replace(tzinfo=None), sample["price"]])


class AnalyticsCatalog(models.Model):
    _name = "golok.lab.analytics.catalog"
    _description = "Upstox NSE cash-equity reference snapshot"
    _rec_name = "digest"
    _order = "id desc"

    company_id = fields.Many2one("res.company", required=True, index=True, ondelete="cascade")
    review_id = fields.Many2one("golok.lab.source.review", required=True, ondelete="restrict")
    digest = fields.Char(required=True)
    fetched_at = fields.Datetime(required=True)
    size = fields.Integer(required=True)

    _revision_once = models.Constraint("UNIQUE(company_id, review_id, digest)", "This reference revision already exists.")

    @api.model
    def _record_revision(self, entries, review):
        self.env["golok.lab.analytics.config"]._admin()
        review = self.env["golok.lab.source.review"]._authorize("upstox", "historical", "import", bound=review)
        if not 0 < len(entries) <= 20_000:
            raise ValidationError(_("The instrument snapshot is empty or exceeds 20,000 equities."))
        company = self.env.company.id
        digest = sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.env.cr.execute("SELECT id FROM res_company WHERE id = %s FOR UPDATE", [company])
        history = self.sudo().with_context({})
        existing = history.search([("company_id", "=", company), ("review_id", "=", review.id), ("digest", "=", digest)], limit=1)
        if existing:
            return existing.id
        snapshot = history.create({"company_id": company, "review_id": review.id, "digest": digest,
                                   "fetched_at": fields.Datetime.now(), "size": len(entries)})
        values = [
            {"catalog_id": snapshot.id, "instrument_key": key, "symbol": details["symbol"],
             "isin": details["isin"], "lot": details["lot"]}
            for key, details in sorted(entries.items())
        ]
        instruments = self.env["golok.lab.analytics.instrument"].sudo().with_context({})
        for offset in range(0, len(values), 500):
            instruments.create(values[offset:offset + 500])
        return snapshot.id


class AnalyticsInstrument(models.Model):
    _name = "golok.lab.analytics.instrument"
    _description = "Imported Upstox instrument reference"
    _rec_name = "symbol"
    _order = "symbol, id"

    catalog_id = fields.Many2one("golok.lab.analytics.catalog", required=True, index=True, ondelete="cascade")
    company_id = fields.Many2one(related="catalog_id.company_id", store=True, index=True)
    fetched_at = fields.Datetime(related="catalog_id.fetched_at")
    instrument_key = fields.Char(required=True)
    symbol = fields.Char(required=True, index=True)
    isin = fields.Char(required=True, index=True)
    lot = fields.Integer(required=True)

    _key_once = models.Constraint("UNIQUE(catalog_id, instrument_key)", "Duplicate instrument key in reference snapshot.")

    @api.model
    def _access_domain(self, operation):
        domain = super()._access_domain(operation)
        if operation == "read" and not self.env.su:
            domain &= Domain("company_id", "=", self.env.company.id)
            domain &= Domain("catalog_id.review_id.readable_now", "=", True)
        return domain

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        raise AccessError(_("The imported instrument reference is for internal display."))


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
    worker_capture = fields.Boolean(string="Use continuous local V3 worker")
    backfill = fields.Boolean(string="Automatically advance permitted historical plans")
    schedule_research = fields.Boolean(string="Queue descriptive research after backfill")
    credential_state = fields.Char(readonly=True)
    connection = fields.Char(readonly=True)
    historical = fields.Char(readonly=True)
    stream = fields.Char(readonly=True)
    instrument_master = fields.Char(readonly=True)
    reference_symbol = fields.Char(readonly=True)
    reference_isin = fields.Char(readonly=True)
    reference_checked_at = fields.Datetime(readonly=True)
    last_quote = fields.Char(compute="_compute_quote", string="Latest Fresh V3 Price")
    last_observed_at = fields.Datetime(compute="_compute_quote", string="Exchange Observation Time")

    @api.depends_context("company", "uid")
    def _compute_quote(self):
        service = self.env["golok.lab.analytics.config"]
        service._admin()
        config = service._current()
        fresh = self._fresh_quote(config)
        for view in self:
            view.last_quote = config.last_quote if fresh else False
            view.last_observed_at = config.observed_at if fresh else False

    def _fresh_quote(self, config):
        now = fields.Datetime.now()
        if not (config.enabled and config.expires_at and config.expires_at > now and config.observed_at
                and config.sample_review_id and timedelta(0) <= now - config.observed_at <= upstox_analytics.MAX_AGE):
            return False
        try:
            self.env["golok.lab.source.review"]._authorize("upstox", "historical", "analytics_collect",
                                                           bound=config.sample_review_id)
            self.env["golok.lab.holdout"]._reject_days(config.mapping_id.instrument_id, [calendar_day(now)], self.env.company)
        except (AccessError, ValidationError):
            return False
        return True

    @api.model
    def default_get(self, names):
        values = super().default_get(names)
        service = self.env["golok.lab.analytics.config"]
        service._admin()
        config = service._current()
        fresh = self._fresh_quote(config)
        values.update({field: value for field, value in {
            "provider": "upstox" if config.enabled else "offline",
            "mapping_id": config.mapping_id.id, "calendar_id": config.calendar_id.id,
            "backfill": config.backfill, "collect": config.collect, "worker_capture": config.worker_capture,
            "schedule_research": config.schedule_research,
            "connection": config.connection or "UNVERIFIED", "historical": config.historical or "UNVERIFIED",
            "stream": ("STALE_OR_UNAVAILABLE" if config.stream == "FRESH_SAMPLE" and not fresh else config.stream or "UNVERIFIED"),
            "instrument_master": config.instrument_master or "UNVERIFIED",
            "credential_state": (("EXPIRED · " if config.expires_at <= fields.Datetime.now() else "")
                                 + fields.Datetime.to_string(config.expires_at)) if config.envelope else "NOT STORED",
            "reference_symbol": config.reference_symbol, "reference_isin": config.reference_isin,
            "reference_checked_at": config.reference_checked_at,
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
                      "worker_capture": enabled and self.collect and self.worker_capture,
                      "backfill": enabled and self.backfill, "schedule_research": enabled and self.schedule_research,
                      "next_collection": False, "failures": 0, "stream": "UNVERIFIED", "last_quote": False,
                      "connection": "UNVERIFIED" if enabled else "DISABLED", "historical": "UNVERIFIED",
                      "instrument_master": "UNVERIFIED", "reference_symbol": False, "reference_isin": False,
                      "reference_checked_at": False,
                      "observed_at": False, "published_at": False, "received_at": False})
        return self._reload()

    def action_test_connection(self):
        service = self._service()
        service._probe(service._ensure_current())
        return self._reload()

    def action_check_master(self):
        service = self._service()
        record = service._ensure_current()
        instrument = None
        try:
            record._credential()
            review = self.env["golok.lab.source.review"]._authorize("upstox", "historical", "import")
            mapping = service._mapping(record, calendar_day())
            entries = upstox_analytics.instrument_master(self.env["golok.lab.provider.budget"]._reserve)
            with self.env.cr.savepoint():
                self.env["golok.lab.analytics.catalog"]._record_revision(entries, review)
            instrument = entries.get(mapping.token)
            status = ("MASTER_MATCH" if instrument and instrument["isin"] == mapping.isin
                      and instrument["symbol"] == mapping.symbol and instrument["lot"] == mapping.lot else "REVIEW_MAPPING_MISMATCH")
        except AccessError:
            status = "PERMISSION_REQUIRED"
        except ValidationError:
            status = "CATALOG_REJECTED"
        except ProviderError as exc:
            status = str(exc)
        record.write({"instrument_master": status, "reference_checked_at": fields.Datetime.now(),
                      "reference_symbol": instrument["symbol"] if status == "MASTER_MATCH" else False,
                      "reference_isin": instrument["isin"] if status == "MASTER_MATCH" else False})
        return self._reload()

    def action_open_reference(self):
        self._service()
        action = self.env["ir.actions.actions"]._for_xml_id("golok_ai_trading_lab_pro.action_analytics_reference")
        current = self.env["golok.lab.analytics.catalog"]
        try:
            review = self.env["golok.lab.source.review"]._authorize("upstox", "historical", "import")
        except AccessError:
            pass
        else:
            current = current.sudo().search([
                ("company_id", "=", self.env.company.id), ("review_id", "=", review.id),
            ], order="id desc", limit=1)
        action["domain"] = [("catalog_id", "=", current.id)]
        return action

    def action_manage_token(self):
        self._service()
        return {"type": "ir.actions.client", "tag": "golok_lab.analytics_secret",
                "name": _("Upstox Analytics Credential"), "params": {"company_id": self.env.company.id}}

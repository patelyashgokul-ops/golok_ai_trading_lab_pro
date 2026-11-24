import hashlib
import json
from datetime import timezone
from decimal import Decimal
from time import perf_counter
from urllib.parse import urlsplit

from odoo import _, api, fields, models
from odoo.fields import Domain
from odoo.exceptions import AccessError, UserError, ValidationError

from ..services import calendar, fixture_generator, indicators, market_data, research


def _input_digest(bars, revision):
    rows = [[bar.close_time.isoformat(), str(bar.open), str(bar.high), str(bar.low), str(bar.close), bar.volume]
            for bar in bars]
    payload = rows
    if revision:
        payload = {
            "calendar_revision": revision.name,
            "schedule": revision.schedule,
            "bars": [row + [bar.open_time.isoformat(), bar.available_at.isoformat()] for row, bar in zip(rows, bars)],
        }
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


class ExchangeCalendar(models.Model):
    _name = "golok.lab.calendar"
    _description = "Explicit exchange calendar revision"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    exchange = fields.Selection([("NSE", "NSE"), ("BSE", "BSE")], required=True)
    source = fields.Char(required=True)
    verification = fields.Selection([("reviewed", "Operator reviewed official source"), ("fixture", "Synthetic calendar")], required=True)
    verified_on = fields.Date(required=True)
    schedule = fields.Text(required=True)

    _version = models.Constraint("UNIQUE(company_id, exchange, name)", "Calendar revisions must be unique per exchange.")

    @api.constrains("schedule", "source", "exchange", "verification", "verified_on")
    def _check_schedule(self):
        for revision in self:
            revision._sessions()
            if revision.verified_on > fields.Date.today():
                raise ValidationError(_("The review date cannot be in the future."))
            if revision.verification == "reviewed":
                domains = {"NSE": {"nseindia.com", "www.nseindia.com", "nsearchives.nseindia.com", "archives.nseindia.com"},
                           "BSE": {"bseindia.com", "www.bseindia.com"}}
                try:
                    location = urlsplit(revision.source)
                    valid = (location.scheme == "https" and location.netloc.lower() in domains[revision.exchange]
                             and bool(location.path.strip("/")))
                except ValueError:
                    valid = False
                if not valid:
                    raise ValidationError(_("A reviewed calendar needs a direct HTTPS source on the official exchange website."))

    def _sessions(self):
        self.ensure_one()
        try:
            return calendar.load_schedule(self.schedule)
        except ValueError as exc:
            raise ValidationError(str(exc)) from None

    def action_generate_fixture(self):
        self.ensure_one()
        self.check_access("read")
        if (self.company_id != self.env.company or self.verification != "fixture"
                or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin")):
            raise AccessError(_("Only an active-company administrator may generate from a fixture calendar."))
        self.env.cr.execute("SELECT id FROM golok_lab_calendar WHERE id=%s FOR UPDATE", (self.id,))
        datasets = self.env["golok.lab.dataset"]
        label = f"Authored {fixture_generator.VERSION} calendar {self.id}"
        result = datasets.search([("company_id", "=", self.company_id.id), ("calendar_id", "=", self.id),
                                  ("fixture_version", "=", fixture_generator.VERSION)], limit=1)
        if not result:
            try:
                sessions = self._sessions()
                now = fields.Datetime.now().replace(tzinfo=timezone.utc)
                if any(session.closing and session.closing > now for session in sessions.values()):
                    raise ValueError("Choose only completed synthetic sessions.")
                bars = fixture_generator.generate(sessions)
            except ValueError as exc:
                raise ValidationError(str(exc)) from None
            symbol = f"SYN-P08-{self.id}"
            instrument = self.env["golok.lab.instrument"].with_context(active_test=False).search([
                ("company_id", "=", self.company_id.id), ("exchange", "=", self.exchange), ("symbol", "=", symbol)], limit=1)
            if instrument:
                raise ValidationError(_("The reserved synthetic instrument symbol already exists."))
            instrument = self.env["golok.lab.instrument"].create({"name": symbol, "symbol": symbol, "exchange": self.exchange})
            result = datasets.sudo().create({
                "name": label, "source": label, "origin": "synthetic", "interval": "5m",
                "instrument_id": instrument.id, "calendar_id": self.id, "company_id": self.company_id.id,
                "fixture_version": fixture_generator.VERSION, "fixture_seed": fixture_generator.SEED,
                "fixture_digest": _input_digest(bars, self),
            })
            result._import_bars(bars)
        return {"type": "ir.actions.act_window", "res_model": datasets._name,
                "res_id": result.id, "views": [(False, "form")]}


class Instrument(models.Model):
    _name = "golok.lab.instrument"
    _description = "Equity instrument"
    _order = "exchange, symbol, id"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    exchange = fields.Selection([("NSE", "NSE"), ("BSE", "BSE")], required=True, default="NSE")
    symbol = fields.Char(required=True, index=True)
    active = fields.Boolean(default=True)

    _symbol = models.Constraint("UNIQUE(company_id, exchange, symbol)", "The exchange symbol must be unique per company.")

    def write(self, vals):
        if {"company_id", "exchange", "symbol"} & vals.keys():
            raise UserError(_("Instrument identity is immutable. Archive it and register a new instrument."))
        return super().write(vals)


class Dataset(models.Model):
    _name = "golok.lab.dataset"
    _description = "Historical OHLCV dataset"
    _check_company_auto = True
    _order = "name, id"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    instrument_id = fields.Many2one("golok.lab.instrument", required=True, ondelete="restrict", check_company=True)
    source = fields.Char(required=True, help="Dataset publisher or file provenance. Keep account information out of this field.")
    origin = fields.Selection([("imported", "Imported historical"), ("synthetic", "Synthetic fixture"),
                               ("provider", "SmartAPI history (publication unknown)")], required=True)
    interval = fields.Selection([(key, key) for key in market_data.INTERVALS], required=True)
    calendar_id = fields.Many2one("golok.lab.calendar", ondelete="restrict", check_company=True)
    quarantined = fields.Boolean(readonly=True)
    integrity_conflict = fields.Boolean(readonly=True, help="An equivalent source observation materially disagreed.")
    source_review_id = fields.Many2one("golok.lab.source.review", readonly=True, check_company=True, ondelete="restrict")
    publication_basis = fields.Selection([("fixture", "Simulation input"), ("operator", "Operator timestamps"),
                                          ("receipt", "First observed receipt")], readonly=True)
    lineage_status = fields.Selection([
        ("generated_fixture", "Server-generated fixture"), ("simulation", "Simulation input"),
        ("insufficient", "Insufficient evidence"), ("active", "Bound source review"),
        ("revoked", "Revoked"), ("authorization_expired", "Authorization expired"),
        ("retention_expired", "Retention expired"), ("quarantined", "Quarantined"),
    ], compute="_compute_lineage_status")
    protected_read = fields.Boolean(compute="_compute_protected_read", search="_search_protected_read")
    fixture_version = fields.Char(readonly=True)
    fixture_seed = fields.Integer(readonly=True)
    fixture_digest = fields.Char(readonly=True)
    daily_revision_id = fields.Many2one("golok.lab.daily.import", readonly=True, ondelete="restrict")
    daily_revision_digest = fields.Char(readonly=True)

    _identity = models.Constraint(
        "UNIQUE(company_id, instrument_id, source, origin, interval)", "This source and interval are already registered."
    )

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [dict(vals) for vals in vals_list]
        missing_identity = {key for vals in vals_list for key in ("origin", "source") if key not in vals}
        defaults = self.default_get(list(missing_identity)) if missing_identity else {}
        if any(vals.get("quarantined") or vals.get("integrity_conflict") for vals in vals_list):
            raise ValidationError(_("Use the administrator quarantine operation."))
        for vals in vals_list:
            for key, value in defaults.items():
                vals.setdefault(key, value)
            if not self.env.su and {"source_review_id", "publication_basis", "fixture_version",
                                    "fixture_seed", "fixture_digest", "daily_revision_id", "daily_revision_digest"} & vals.keys():
                raise AccessError(_("Lineage is assigned by the server."))
            if (vals.get("source") or "").startswith("P08 correction ") and not vals.get("daily_revision_id"):
                raise AccessError(_("The source label is reserved for audited corrections."))
            if vals.get("origin") == "imported" and not vals.get("source_review_id"):
                review = self.env["golok.lab.source.review"]._authorize(
                    "manual", "historical", "import", upstream=vals.get("source"))
                vals.update(source_review_id=review.id, publication_basis="operator")
            if vals.get("origin") == "synthetic":
                vals.update(source_review_id=False, publication_basis="fixture")
        return super(Dataset, self.with_context(default_quarantined=False, default_integrity_conflict=False, default_source_review_id=False,
                                                default_publication_basis=False, default_fixture_version=False,
                                                default_fixture_seed=0, default_fixture_digest=False,
                                                default_daily_revision_id=False, default_daily_revision_digest=False)).create(vals_list)

    @api.depends("origin", "fixture_version", "publication_basis", "source_review_id.lifecycle", "quarantined", "integrity_conflict")
    def _compute_lineage_status(self):
        for dataset in self:
            if dataset.quarantined or dataset.integrity_conflict:
                dataset.lineage_status = "quarantined"
            elif dataset.origin == "synthetic":
                dataset.lineage_status = "generated_fixture" if dataset.fixture_version else "simulation"
            else:
                review = dataset.sudo().source_review_id
                lifecycle = review.lifecycle if review else "insufficient"
                if lifecycle == "transient" or (lifecycle == "active" and not dataset.publication_basis):
                    lifecycle = "insufficient"
                dataset.lineage_status = lifecycle

    def _search_protected_read(self, operator, value):
        if operator != "in" or tuple(value) != (True,):
            return NotImplemented
        return (Domain("origin", "=", "synthetic")
                | (Domain("publication_basis", "in", ["operator", "receipt"])
                   & Domain("source_review_id", "any!", Domain("readable_now", "=", True))))

    @api.depends("origin", "publication_basis", "source_review_id.readable_now")
    def _compute_protected_read(self):
        for dataset in self:
            dataset.protected_read = dataset.origin == "synthetic" or (
                dataset.publication_basis in ("operator", "receipt") and dataset.sudo().source_review_id.readable_now)

    def _permit(self, purpose):
        self.ensure_one()
        if (not self.env.su and self.company_id != self.env.company) or self.quarantined or self.integrity_conflict:
            raise AccessError(_("The dataset is unavailable for this operation."))
        if self.origin == "synthetic" and purpose in ("import", "research"):
            return
        review = self.sudo().source_review_id
        if not review or self.publication_basis not in ("operator", "receipt"):
            raise AccessError(_("The historical dataset has no effective authorization lineage."))
        if review.provider not in ("smartapi", "bhavcopy", "manual"):
            raise AccessError(_("The data is ineligible for this operation."))
        return self.env["golok.lab.source.review"]._authorize(
            review.provider, "daily" if review.provider == "bhavcopy" else "historical", purpose,
            upstream=self.source, bound=review)

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        self.check_access("read")
        if any(record.origin != "synthetic" for record in self):
            raise AccessError(_("Historical market dataset exports are disabled."))
        return super()._export_rows(fields, _is_toplevel_call=_is_toplevel_call)

    @api.constrains("calendar_id", "instrument_id", "origin")
    def _check_calendar(self):
        for dataset in self.filtered("calendar_id"):
            if dataset.calendar_id.exchange != dataset.instrument_id.exchange:
                raise ValidationError(_("The calendar and instrument exchanges must match."))
            if dataset.calendar_id.verification == "fixture" and dataset.origin != "synthetic":
                raise ValidationError(_("Only synthetic datasets may use fixture calendars."))

    def write(self, vals):
        allowed = {"name", "quarantined"} | ({"integrity_conflict"} if self.env.su else set())
        if set(vals) - allowed:
            raise UserError(_("Dataset provenance is immutable. Register a new dataset for a new source."))
        if "quarantined" in vals and not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise ValidationError(_("Only a Trading System Administrator may change dataset quarantine."))
        return super().write(vals)

    def action_toggle_quarantine(self):
        self.ensure_one()
        self.check_access("write")
        self.write({"quarantined": not self.quarantined})

    def _import_bars(self, bars):
        self.ensure_one()
        self.check_access("write")
        if (self.fixture_version or self.daily_revision_id) and not self.env.su:
            raise AccessError(_("Generated and corrected observations are immutable."))
        if self.quarantined:
            raise ValidationError(_("The dataset is quarantined."))
        self._permit("import")
        if self.calendar_id:
            sessions = self.calendar_id._sessions()
            try:
                for bar in bars:
                    calendar.validate_bar(bar, sessions, market_data.INTERVALS[self.interval])
            except ValueError as exc:
                raise ValidationError(str(exc)) from None
        elif any(bar.open_time or bar.available_at for bar in bars):
            raise ValidationError(_("Temporal bars require a calendar revision."))
        model = self.env["golok.lab.candle"]
        rows = {bar.close_time.replace(tzinfo=None): bar for bar in bars}
        existing = model.search([("dataset_id", "=", self.id), ("close_time", "in", list(rows))])
        for candle in existing:
            if candle._to_bar() != rows.pop(candle.close_time):
                raise ValidationError(_("A stored candle differs from the import. No candles were imported."))
        # The unique index is the final arbiter if two transactions race.
        model.with_context({}).sudo().create([
            {
                "dataset_id": self.id,
                "close_time": timestamp,
                "open_time": bar.open_time.replace(tzinfo=None) if bar.open_time else False,
                "available_at": bar.available_at.replace(tzinfo=None) if bar.available_at else False,
                "open_price": str(bar.open),
                "high_price": str(bar.high),
                "low_price": str(bar.low),
                "close_price": str(bar.close),
                "volume": bar.volume,
                "processing_version": "2" if self.calendar_id else market_data.VERSION,
            }
            for timestamp, bar in rows.items()
        ])
        return len(rows)


class Candle(models.Model):
    _name = "golok.lab.candle"
    _description = "Validated historical candle"
    _check_company_auto = True
    _order = "close_time desc, id desc"

    dataset_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="dataset_id.company_id", store=True, index=True)
    instrument_id = fields.Many2one(related="dataset_id.instrument_id", store=True, index=True)
    exchange = fields.Selection(related="dataset_id.instrument_id.exchange")
    source = fields.Char(related="dataset_id.source")
    origin = fields.Selection(related="dataset_id.origin")
    interval = fields.Selection(related="dataset_id.interval")
    close_time = fields.Datetime(required=True)
    open_time = fields.Datetime()
    available_at = fields.Datetime()
    ingested_at = fields.Datetime(required=True, default=fields.Datetime.now, index=True)
    # Capture the imported decimal representation without binary rounding.
    open_price = fields.Char(required=True)
    high_price = fields.Char(required=True)
    low_price = fields.Char(required=True)
    close_price = fields.Char(required=True)
    volume = fields.Integer(required=True)
    processing_version = fields.Char(required=True, default=market_data.VERSION)
    quality = fields.Selection([("validated", "OHLCV validated")], required=True, default="validated")

    _unique_bar = models.Constraint("UNIQUE(dataset_id, close_time)", "A candle already exists for this close time.")
    _valid_volume = models.Constraint("CHECK(volume >= 0)", "Volume cannot be negative.")
    _time_order = models.Constraint(
        "CHECK ((open_time IS NULL AND available_at IS NULL) OR "
        "(open_time IS NOT NULL AND available_at IS NOT NULL AND open_time < close_time AND close_time <= available_at))",
        "Opening and availability timestamps must bracket the close.",
    )

    def _to_bar(self):
        self.ensure_one()
        return market_data.Candle(
            self.close_time.replace(tzinfo=timezone.utc),
            Decimal(self.open_price), Decimal(self.high_price),
            Decimal(self.low_price), Decimal(self.close_price), self.volume,
            self.open_time.replace(tzinfo=timezone.utc) if self.open_time else None,
            self.available_at.replace(tzinfo=timezone.utc) if self.available_at else None,
        )

    @api.model
    def _access_domain(self, operation):
        domain = super()._access_domain(operation)
        if operation == "read" and not self.env.su:
            domain &= self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id")
        return domain

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        self.check_access("read")
        if any(row.dataset_id.origin != "synthetic" for row in self):
            raise AccessError(_("Historical market observations are not exportable."))
        return super()._export_rows(fields, _is_toplevel_call=_is_toplevel_call)


class ResearchRun(models.Model):
    _name = "golok.lab.run"
    _description = "Historical research snapshot"
    _check_company_auto = True
    _order = "id desc"

    dataset_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", check_company=True)
    company_id = fields.Many2one(related="dataset_id.company_id", store=True, index=True)
    as_of = fields.Datetime(required=True, string="Cutoff")
    first_close = fields.Datetime()
    last_close = fields.Datetime(index=True)
    origin = fields.Selection(related="dataset_id.origin")
    bar_count = fields.Integer()
    gap_count = fields.Integer(string="Intraday gaps")
    input_digest = fields.Char(string="Input SHA-256", required=True)
    engine_version = fields.Char(required=True)
    evidence = fields.Json()
    evidence_text = fields.Text(compute="_compute_evidence_text")
    decision = fields.Selection([("no_trade", "NO TRADE")], default="no_trade", required=True)
    reason = fields.Char(required=True)

    _snapshot = models.Constraint(
        "UNIQUE(dataset_id, as_of, engine_version, input_digest)", "This research snapshot already exists."
    )

    @api.model
    def _access_domain(self, operation):
        domain = super()._access_domain(operation)
        if operation == "read" and not self.env.su:
            domain &= self.env["golok.lab.holdout"]._observation_domain(
                "first_close", "last_close", "dataset_id.instrument_id")
        return domain

    @api.depends("evidence")
    def _compute_evidence_text(self):
        for run in self:
            run.evidence_text = json.dumps(run.evidence or {}, indent=2)

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        started = perf_counter()
        if len(vals_list) != 1 or set(vals_list[0]) != {"dataset_id", "as_of"}:
            raise ValidationError(_("Supply one dataset and one cutoff. Research results are computed by the server."))
        request = vals_list[0]
        dataset_id = request["dataset_id"]
        if type(dataset_id) is not int or dataset_id <= 0:
            raise ValidationError(_("Select one valid dataset."))
        dataset = self.env["golok.lab.dataset"].search([("id", "=", dataset_id)], limit=1)
        if not dataset:
            # Use a uniform response for absent and inaccessible records.
            raise AccessError(_("Dataset is unavailable."))
        try:
            cutoff = fields.Datetime.to_datetime(request["as_of"])
        except (TypeError, ValueError):
            cutoff = None
        if not cutoff or cutoff.tzinfo is not None or cutoff > fields.Datetime.now():
            raise ValidationError(_("The research cutoff must be present and no later than now."))
        if dataset.quarantined:
            raise ValidationError(_("The dataset is quarantined."))
        dataset._permit("research")
        self.env["golok.lab.replay.guard"]._lock(dataset.instrument_id)
        domain = [("dataset_id", "=", dataset.id), ("close_time", "<=", cutoff)]
        if dataset.calendar_id:
            domain.append(("available_at", "<=", cutoff))
        candle_model = self.env["golok.lab.candle"]
        isolation = self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id")
        candles = candle_model.search(Domain(domain) & isolation, limit=250)
        bars = [candle._to_bar() for candle in reversed(candles)]
        version = "2" if dataset.calendar_id else research.VERSION
        digest = _input_digest(bars, dataset.calendar_id)
        quality_warning = None
        sessions = None
        if dataset.calendar_id:
            sessions = dataset.calendar_id._sessions()
            try:
                gaps = calendar.missing_observations(bars, sessions, market_data.INTERVALS[dataset.interval])
            except ValueError as exc:
                gaps = 0
                quality_warning = str(exc)
        else:
            gaps = market_data.check_series(bars, dataset.interval)
        if gaps:
            quality_warning = "Missing observations in selected window"
        values = research.describe(bars) if not quality_warning else {}
        status = "INSUFFICIENT_DATA"
        evidence = {}
        metric_keys = ("sma20", "relative_volume20", "atr14")
        for engine, metric in zip(research.ENGINES, metric_keys):
            value = values.get(metric)
            evidence[engine] = {
                "version": research.VERSION,
                "method": metric,
                "required_input": "Validated historical OHLCV",
                "status": "COMPLETED" if value is not None else status,
                "finding": str(value) if value is not None else None,
                "quality_warning": quality_warning,
            }
        if dataset.calendar_id:
            series = indicators.calculate(bars, sessions=sessions) if bars and not quality_warning else {}
            groups = {"RE-01": ("ema20", "rsi14", "macd", "adx14", "stochastic14", "roc10", "trend_slope20",
                                "high_low20", "opening_range15", "relative_strength", "gap"),
                      "RE-05": ("vwap", "obv", "volume_spike"),
                      "RE-18": ("volatility20", "bollinger20")}
            elapsed = round(1000 * (perf_counter() - started), 3)
            for key, finding in evidence.items():
                finding.update({
                    "version": "2", "engine_id": key, "input_digest": digest, "dataset": dataset.id,
                    "instrument": dataset.instrument_id.id, "cutoff_utc": fields.Datetime.to_string(cutoff),
                    "source": dataset.source, "origin": dataset.origin, "freshness": "historical_only",
                    "supporting_evidence": {"bars": len(bars), "gaps": gaps},
                    "contradictory_evidence": [quality_warning] if quality_warning else [],
                    "missing_inputs": [] if finding["finding"] is not None else ["Eligible sample for primary finding"],
                    "limits": ["Source availability supplied by the operator", "Research only"],
                    "applicable_strategies": [], "snapshot_duration_ms": elapsed,
                    "indicators": {name: str(series[name][-1]) if series[name][-1] is not None else None
                                   for name in groups[key]} if series else {},
                })
        identity = {"dataset_id": dataset.id, "as_of": cutoff, "input_digest": digest, "engine_version": version}
        prior = self.search([(key, "=", val) for key, val in identity.items()], limit=1)
        if prior:
            return prior
        return super().create([{
            **identity,
            "first_close": candles[-1:].close_time,
            "last_close": candles[:1].close_time,
            "bar_count": len(bars),
            "gap_count": gaps,
            "evidence": evidence,
            "reason": _("Historical research only. No validated actionable strategy or live feed."),
        }])

    @api.model
    def overview(self):
        self.check_access("read")
        domain = [("company_id", "=", self.env.company.id)]
        last = self.search(domain, limit=1)
        candle_model = self.env["golok.lab.candle"]
        current_ingest = candle_model.search(domain, order="ingested_at desc, id desc", limit=1)
        return {
            "company_id": self.env.company.id,
            "company_name": self.env.company.display_name,
            "instruments": self.env["golok.lab.instrument"].search_count([*domain, ("active", "=", True)]),
            "datasets": self.env["golok.lab.dataset"].search_count(domain),
            "candles": candle_model.search_count(domain),
            "last_ingestion": fields.Datetime.to_string(current_ingest.ingested_at) if current_ingest else False,
            "quarantined": self.env["golok.lab.dataset"].search_count([*domain, ("quarantined", "=", True)]),
            "runs": self.search_count(domain),
            "last": last.read(["dataset_id", "as_of", "last_close", "bar_count", "gap_count", "reason", "origin"])[0]
            if last else None,
        }

    @api.model
    def chart_data(self, run_id):
        self.check_access("read")
        if type(run_id) is not int or run_id <= 0:
            return None
        run = self.search([("id", "=", run_id), ("company_id", "=", self.env.company.id)], limit=1)
        if not run:
            return None
        candles = run._checked_snapshot_candles()
        if not candles:
            return None
        return {"origin": run.origin, "bars": [
            [fields.Datetime.to_string(row.close_time), row.open_price, row.high_price,
             row.low_price, row.close_price, row.volume] for row in reversed(candles[:60])
        ]}

    def _checked_snapshot_candles(self):
        self.ensure_one()
        self.check_access("read")
        run = self
        if not run.last_close or run.dataset_id.quarantined:
            return self.env["golok.lab.candle"]
        run.dataset_id._permit("research")
        domain = [("dataset_id", "=", run.dataset_id.id), ("close_time", ">=", run.first_close),
                  ("close_time", "<=", run.last_close)]
        if run.engine_version == "2":
            domain.append(("available_at", "<=", run.as_of))
        candles = self.env["golok.lab.candle"].search(domain, limit=251)
        if len(candles) != run.bar_count or _input_digest(
            [row._to_bar() for row in reversed(candles)], run.dataset_id.calendar_id
        ) != run.input_digest:
            return self.env["golok.lab.candle"]
        return candles

    def _export_rows(self, fields, *, _is_toplevel_call=True):
        self.check_access("read")
        if any(row.dataset_id.origin != "synthetic" for row in self):
            raise AccessError(_("Historical market research is not exportable."))
        return super()._export_rows(fields, _is_toplevel_call=_is_toplevel_call)

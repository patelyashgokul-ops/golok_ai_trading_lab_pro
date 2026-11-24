import hashlib
import json
from datetime import timezone
from decimal import Decimal

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..services import market_data, research


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
    origin = fields.Selection([("imported", "Imported historical"), ("synthetic", "Synthetic fixture")], required=True)
    interval = fields.Selection([(key, key) for key in market_data.INTERVALS], required=True)

    _identity = models.Constraint(
        "UNIQUE(company_id, instrument_id, source, origin, interval)", "This source and interval are already registered."
    )

    def write(self, vals):
        if set(vals) - {"name"}:
            raise UserError(_("Dataset provenance is immutable. Register a new dataset for a new source."))
        return super().write(vals)

    def _import_bars(self, bars):
        self.ensure_one()
        self.check_access("write")
        model = self.env["golok.lab.candle"]
        rows = {bar.close_time.replace(tzinfo=None): bar for bar in bars}
        existing = model.search([("dataset_id", "=", self.id), ("close_time", "in", list(rows))])
        for candle in existing:
            if candle._to_bar() != rows.pop(candle.close_time):
                raise ValidationError(_("A stored candle differs from the import. No candles were imported."))
        # The unique index is the final arbiter if two transactions race.
        model.sudo().create([
            {
                "dataset_id": self.id,
                "close_time": timestamp,
                "open_price": str(bar.open),
                "high_price": str(bar.high),
                "low_price": str(bar.low),
                "close_price": str(bar.close),
                "volume": bar.volume,
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
    ingested_at = fields.Datetime(required=True, default=fields.Datetime.now)
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

    def _to_bar(self):
        self.ensure_one()
        return market_data.Candle(
            self.close_time.replace(tzinfo=timezone.utc),
            Decimal(self.open_price), Decimal(self.high_price),
            Decimal(self.low_price), Decimal(self.close_price), self.volume,
        )


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
    decision = fields.Selection([("no_trade", "NO TRADE")], default="no_trade", required=True)
    reason = fields.Char(required=True)

    _snapshot = models.Constraint(
        "UNIQUE(dataset_id, as_of, engine_version, input_digest)", "This research snapshot already exists."
    )

    @api.model_create_multi
    def create(self, vals_list):
        if len(vals_list) != 1 or set(vals_list[0]) != {"dataset_id", "as_of"}:
            raise ValidationError(_("Supply one dataset and one cutoff. Research results are computed by the server."))
        request = vals_list[0]
        dataset = self.env["golok.lab.dataset"].browse(request["dataset_id"]).exists()
        if not dataset:
            raise ValidationError(_("Dataset does not exist."))
        dataset.ensure_one()
        dataset.check_access("read")
        cutoff = fields.Datetime.to_datetime(request["as_of"])
        if not cutoff or cutoff > fields.Datetime.now():
            raise ValidationError(_("The research cutoff must be present and no later than now."))
        candles = self.env["golok.lab.candle"].search(
            [("dataset_id", "=", dataset.id), ("close_time", "<=", cutoff)], limit=250,
        )
        bars = [candle._to_bar() for candle in reversed(candles)]
        payload = [
            [bar.close_time.isoformat(), str(bar.open), str(bar.high), str(bar.low), str(bar.close), bar.volume]
            for bar in bars
        ]
        digest = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()
        gaps = market_data.check_series(bars, dataset.interval)
        values = research.describe(bars) if not gaps else {}
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
                "quality_warning": "Intraday gaps in selected window" if gaps else None,
            }
        identity = {"dataset_id": dataset.id, "as_of": cutoff, "input_digest": digest, "engine_version": research.VERSION}
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
        return {
            "instruments": self.env["golok.lab.instrument"].search_count(domain),
            "datasets": self.env["golok.lab.dataset"].search_count(domain),
            "candles": self.env["golok.lab.candle"].search_count(domain),
            "runs": self.search_count(domain),
            "last": last.read(["dataset_id", "as_of", "last_close", "bar_count", "gap_count", "reason", "origin"])[0]
            if last else None,
        }

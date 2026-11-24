from datetime import timezone
from decimal import Decimal, InvalidOperation

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..services import calendar, reference


class InstrumentMapping(models.Model):
    _name = "golok.lab.mapping"
    _description = "Effective-dated equity mapping"
    _rec_name = "symbol"
    _order = "starts desc, id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    instrument_id = fields.Many2one("golok.lab.instrument", required=True, ondelete="restrict", check_company=True)
    exchange = fields.Selection([("NSE", "NSE"), ("BSE", "BSE")], required=True, readonly=True)
    segment = fields.Selection([("equity", "Cash equity")], required=True, default="equity")
    symbol = fields.Char(required=True)
    provider = fields.Selection([("smartapi", "Angel One SmartAPI"), ("manual", "Manual reference")], required=True)
    token = fields.Char(required=True)
    starts = fields.Date(required=True)
    ends = fields.Date(help="Exclusive end date. Set a finite end if token or symbol reuse is known.")
    tick = fields.Char(required=True, help="Exact decimal value, for example 0.05.")
    lot = fields.Integer(required=True, default=1)
    listing_status = fields.Selection([("listed", "Listed"), ("suspended", "Suspended"), ("delisted", "Delisted")], required=True)
    source = fields.Char(required=True)
    revision = fields.Char(required=True)
    verification = fields.Selection([("reviewed", "Operator reviewed"), ("unverified", "Unverified"),
                                     ("fixture", "Synthetic fixture")], required=True)
    isin = fields.Char()
    sector = fields.Char()

    _date_order = models.Constraint("CHECK (ends IS NULL OR ends > starts)", "Mapping dates must be increasing.")
    _token_overlap = models.Constraint(
        "EXCLUDE USING gist (company_id WITH =, exchange WITH =, provider WITH =, token WITH =, "
        "daterange(starts, ends, '[)') WITH &&)", "Provider token dates overlap.")
    _symbol_overlap = models.Constraint(
        "EXCLUDE USING gist (company_id WITH =, exchange WITH =, provider WITH =, lower(symbol) WITH =, "
        "daterange(starts, ends, '[)') WITH &&)", "Provider symbol dates overlap.")
    _instrument_overlap = models.Constraint(
        "EXCLUDE USING gist (instrument_id WITH =, provider WITH =, daterange(starts, ends, '[)') WITH &&)",
        "Instrument mapping dates overlap.")

    def _auto_init(self):
        self.env.cr.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
        return super()._auto_init()

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        prepared = []
        for vals in vals_list:
            instrument_id = vals.get("instrument_id")
            if type(instrument_id) is not int or instrument_id <= 0:
                raise ValidationError(_("Select an instrument."))
            instrument = self.env["golok.lab.instrument"].browse(instrument_id)
            instrument.check_access("read")
            if vals.get("company_id", instrument.company_id.id) != instrument.company_id.id:
                raise ValidationError(_("The mapping must use the instrument's company."))
            prepared.append({**vals, "exchange": instrument.exchange, "company_id": instrument.company_id.id})
        return super().create(prepared)

    @api.constrains("token", "starts", "ends", "tick", "lot", "isin", "symbol", "source", "revision")
    def _check_reference(self):
        for row in self:
            try:
                reference.Mapping(str(row.instrument_id.id), row.exchange, row.symbol, row.provider, row.token,
                                  row.starts, row.ends or None, Decimal(row.tick), row.lot, row.listing_status,
                                  row.source, row.revision, row.verification, row.isin or None, row.sector or None)
            except (TypeError, ValueError, InvalidOperation) as exc:
                raise ValidationError(_("Invalid instrument mapping details.")) from exc

    def _covers(self, day, origin):
        self.ensure_one()
        expected = "fixture" if origin == "synthetic" else "reviewed"
        return (self.starts <= day and (not self.ends or day < self.ends)
                and self.listing_status == "listed" and self.verification == expected)


class CorporateAction(models.Model):
    _name = "golok.lab.corporate.action"
    _description = "Corporate action source record"
    _order = "effective desc, id desc"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    instrument_id = fields.Many2one("golok.lab.instrument", required=True, ondelete="restrict", check_company=True)
    kind = fields.Selection([("split", "Stock split"), ("bonus", "Bonus issue"), ("symbol", "Symbol change"),
                             ("suspension", "Suspension"), ("listing", "Listing"), ("delisting", "Delisting")],
                            required=True)
    effective = fields.Date(required=True)
    published_at = fields.Datetime(required=True)
    source = fields.Char(required=True)
    revision = fields.Char(required=True)
    numerator = fields.Integer(help="New shares in the adjustment ratio.")
    denominator = fields.Integer(help="Old shares in the adjustment ratio.")

    _revision = models.Constraint("UNIQUE(instrument_id, kind, effective, revision)", "Corporate action revision already exists.")
    _ratio = models.Constraint(
        "CHECK (CASE WHEN kind IN ('split','bonus') THEN numerator IS NOT NULL AND denominator IS NOT NULL "
        "AND numerator > 0 AND denominator > 0 ELSE COALESCE(numerator,0) = 0 AND COALESCE(denominator,0) = 0 END)",
        "Only splits and bonus issues require positive share ratios.")

    @api.constrains("published_at", "source", "revision")
    def _check_source(self):
        for row in self:
            if row.published_at > fields.Datetime.now() or not row.source.strip() or not row.revision.strip():
                raise ValidationError(_("A corporate action needs a non-future publication timestamp and source revision."))


class MappedDataset(models.Model):
    _inherit = "golok.lab.dataset"

    mapping_id = fields.Many2one("golok.lab.mapping", ondelete="restrict", check_company=True)

    @api.constrains("mapping_id", "instrument_id", "calendar_id", "origin")
    def _check_reference_scope(self):
        for dataset in self.filtered("mapping_id"):
            if dataset.mapping_id.instrument_id != dataset.instrument_id or not dataset.calendar_id:
                raise ValidationError(_("Use a calendar-bound dataset and a mapping of the same instrument."))
            if not dataset.mapping_id._covers(dataset.mapping_id.starts, dataset.origin):
                raise ValidationError(_("The mapping must be listed and match the dataset's provenance category."))

    def _import_bars(self, bars):
        self.ensure_one()
        self.check_access("write")
        if self.mapping_id:
            tick = Decimal(self.mapping_id.tick)
            for bar in bars:
                day = bar.close_time.astimezone(calendar.IST).date()
                if not self.mapping_id._covers(day, self.origin):
                    raise ValidationError(_("A candle is outside the mapping's effective dates."))
                if any(price % tick for price in (bar.open, bar.high, bar.low, bar.close)):
                    raise ValidationError(_("A candle price is outside the instrument's tick grid."))
        return super()._import_bars(bars)

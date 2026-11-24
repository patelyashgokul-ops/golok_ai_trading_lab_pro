import hashlib
import json
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import backtest, calendar, experiments, market_data, simulation


class StrategyVersion(models.Model):
    _name = "golok.lab.strategy"
    _description = "Research strategy version"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    version = fields.Char(required=True)
    state = fields.Selection([("research", "Synthetic research only")], required=True, default="research")

    _identity = models.Constraint("UNIQUE(code,version)", "Strategy version already exists.")


class TariffPlan(models.Model):
    _name = "golok.lab.tariff"
    _description = "Hypothetical tariff revision"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    lines = fields.Text(required=True, string="Hypothetical tariff JSON")

    _identity = models.Constraint("UNIQUE(company_id,name)", "Tariff revision names must be unique.")

    @api.constrains("lines")
    def _check_lines(self):
        for plan in self:
            plan._schedule()

    def _schedule(self):
        self.ensure_one()
        try:
            return experiments.read_tariffs(self.lines)
        except ValueError as exc:
            raise ValidationError(str(exc)) from None


class Experiment(models.Model):
    _name = "golok.lab.experiment"
    _description = "Immutable synthetic experiment"
    _rec_name = "fingerprint"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    dataset_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict", check_company=True)
    strategy_id = fields.Many2one("golok.lab.strategy", required=True, ondelete="restrict")
    tariff_id = fields.Many2one("golok.lab.tariff", required=True, ondelete="restrict", check_company=True)
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    capital = fields.Char(required=True)
    tick = fields.Char(required=True)
    status = fields.Selection([("completed", "Synthetic completed"), ("unresolved", "Synthetic unresolved")], required=True)
    fingerprint = fields.Char(required=True)
    trade_count = fields.Integer()
    candidate_count = fields.Integer()
    specification = fields.Text(required=True)
    result = fields.Text(required=True)

    _fingerprint = models.Constraint("UNIQUE(company_id,fingerprint)", "Experiment already exists.")

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        accepted = {"dataset_id", "strategy_id", "tariff_id", "starts", "ends", "capital", "tick"}
        if len(vals_list) != 1 or set(vals_list[0]) != accepted:
            raise ValidationError(_("Supply one experiment input and no generated fields."))
        vals = vals_list[0]
        company = self.env.company
        records = []
        for key, model in (("dataset_id", "golok.lab.dataset"), ("strategy_id", "golok.lab.strategy"),
                           ("tariff_id", "golok.lab.tariff")):
            identifier = vals[key]
            if type(identifier) is not int or identifier <= 0:
                raise ValidationError(_("Select valid experiment records."))
            domain = [("id", "=", identifier)]
            if key != "strategy_id":
                domain.append(("company_id", "=", company.id))
            record = self.env[model].search(domain, limit=1)
            if not record:
                raise AccessError(_("Experiment input unavailable."))
            records.append(record)
        dataset, strategy, tariff = records
        if dataset.origin != "synthetic" or not dataset.calendar_id or dataset.quarantined:
            raise ValidationError(_("Use an eligible calendar-bound synthetic dataset."))
        if strategy != self.env.ref("golok_ai_trading_lab_pro.strategy_st01_p03"):
            raise ValidationError(_("Unsupported strategy version."))
        seconds = market_data.INTERVALS[dataset.interval]
        if seconds not in (60, 180, 300, 900):
            raise ValidationError(_("Use a 1, 3, 5 or 15 minute dataset."))
        try:
            starts, ends = fields.Date.to_date(vals["starts"]), fields.Date.to_date(vals["ends"])
            if (not starts or not ends or ends > fields.Date.today()
                    or not 0 <= (ends - starts).days < experiments.MAX_DAYS):
                raise ValueError
            if not all(isinstance(vals[key], str) and market_data.NUMBER.fullmatch(vals[key]) for key in ("capital", "tick")):
                raise ValueError
            capital, tick = Decimal(vals["capital"]), Decimal(vals["tick"])
            if (not capital.is_finite() or not tick.is_finite() or not 0 < capital <= 100_000_000
                    or not Decimal("0.000001") <= tick <= 10000):
                raise ValueError
        except (TypeError, ValueError, InvalidOperation):
            raise ValidationError(_("Use at most 31 valid dates and positive decimal capital and tick values.")) from None
        if dataset.mapping_id and tick != Decimal(dataset.mapping_id.tick):
            raise ValidationError(_("Use the stored mapping tick size."))
        opening = datetime.combine(starts, time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        ending = datetime.combine(ends + timedelta(days=1), time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        bars = self.env["golok.lab.candle"].search(
            [("dataset_id", "=", dataset.id), ("close_time", ">=", opening), ("close_time", "<", ending)],
            order="close_time", limit=experiments.MAX_BARS + 1,
        )
        if len(bars) > experiments.MAX_BARS:
            raise ValidationError(_("Narrow the experiment to 4,000 or fewer candles."))
        output = experiments.simulate([bar._to_bar() for bar in bars], dataset.calendar_id._sessions(), starts, ends,
                                      dataset.instrument_id.exchange, seconds, tick, tariff._schedule(),
                                      dataset.source, simulation.RiskPolicy(capital=capital))
        spec = output["specification"]
        spec.update({"dataset": dataset.id, "calendar": dataset.calendar_id.id, "tariff": tariff.id,
                     "strategy_version": strategy.version, "company": company.id,
                     "calendar_digest": hashlib.sha256(dataset.calendar_id.schedule.encode()).hexdigest(),
                     "code_digest": hashlib.sha256(Path(experiments.__file__).read_bytes()).hexdigest()})
        fingerprint = hashlib.sha256(backtest.canonical(spec).encode()).hexdigest()
        prior = self.search([("company_id", "=", company.id), ("fingerprint", "=", fingerprint)], limit=1)
        if prior:
            return prior
        return super(Experiment, self.with_context({})).create([{
            **vals, "company_id": company.id, "status": output["status"], "fingerprint": fingerprint,
            "trade_count": output["metrics"]["trades"], "candidate_count": output["metrics"]["considered"],
            "specification": json.dumps(spec, default=str, indent=2, sort_keys=True),
            "result": json.dumps(output, default=str, indent=2, sort_keys=True),
        }])

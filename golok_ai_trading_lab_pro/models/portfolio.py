import hashlib
import json
from dataclasses import asdict
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import backtest, calendar, decision, eligibility, market_data, portfolio, simulation, strategies


def digest(value):
    return hashlib.sha256(backtest.canonical(value).encode()).hexdigest()


STRATEGIES = [("all", "All experimental strategies"), *((key, key) for key in strategies.REGISTRY)]


class Portfolio(models.Model):
    _name = "golok.lab.portfolio"
    _description = "Immutable synthetic portfolio replay"
    _rec_name = "fingerprint"
    _order = "id desc"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    dataset_ids = fields.Many2many("golok.lab.dataset", check_company=True)
    tariff_id = fields.Many2one("golok.lab.tariff", required=True, ondelete="restrict", check_company=True)
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    capital = fields.Char(required=True)
    tick = fields.Char(required=True)
    strategy = fields.Selection(STRATEGIES, required=True)
    fingerprint = fields.Char(required=True)
    trade_count = fields.Integer()
    decision_count = fields.Integer()
    suspended = fields.Boolean()
    specification = fields.Text(required=True)
    result = fields.Text(required=True)

    _fingerprint = models.Constraint("UNIQUE(company_id,fingerprint)", "This portfolio already exists.")

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        allowed = {"dataset_ids", "tariff_id", "starts", "ends", "capital", "tick", "strategy"}
        if len(vals_list) != 1 or set(vals_list[0]) != allowed:
            raise ValidationError(_("Supply one portfolio request with no generated fields."))
        vals = vals_list[0]
        identifiers, tariff_id = vals["dataset_ids"], vals["tariff_id"]
        if (not isinstance(identifiers, (tuple, list)) or not 1 <= len(identifiers) <= portfolio.MAX_INSTRUMENTS
                or any(type(item) is not int or item <= 0 for item in identifiers)
                or len(set(identifiers)) != len(identifiers) or type(tariff_id) is not int or tariff_id <= 0):
            raise ValidationError(_("Select up to 16 distinct datasets and one hypothetical tariff."))
        company = self.env.company
        datasets = self.env["golok.lab.dataset"].search(
            [("id", "in", identifiers), ("company_id", "=", company.id)], order="id")
        tariff = self.env["golok.lab.tariff"].search([("id", "=", tariff_id), ("company_id", "=", company.id)])
        if len(datasets) != len(identifiers) or not tariff:
            raise AccessError(_("Portfolio inputs are unavailable for the active company."))
        if (len(datasets.instrument_id) != len(datasets) or len(set(datasets.mapped("interval"))) != 1
                or any(not dataset.calendar_id or not eligibility.evaluate(
                    dataset.origin, "synthetic_replay", quarantined=dataset.quarantined)[1]
                    for dataset in datasets)):
            raise ValidationError(_("Select calendar-bound eligible synthetic datasets with distinct instruments and one interval."))
        starts, ends, capital, tick = self._parse_request(vals)
        code = vals["strategy"]
        codes = tuple(sorted(strategies.REGISTRY)) if code == "all" else (code,)
        seconds = market_data.INTERVALS[datasets[0].interval]
        opening = datetime.combine(starts, time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        ending = datetime.combine(ends + timedelta(days=1), time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        assets, inputs = [], []
        remaining = portfolio.MAX_BARS
        for dataset in datasets:
            candles = self.env["golok.lab.candle"].search(
                [("dataset_id", "=", dataset.id), ("close_time", ">=", opening), ("close_time", "<", ending)],
                order="close_time", limit=remaining + 1)
            if len(candles) > remaining:
                raise ValidationError(_("Narrow the portfolio to 12,000 or fewer observations."))
            remaining -= len(candles)
            revision = dataset.calendar_id
            instrument = dataset.instrument_id
            asset_tick = Decimal(dataset.mapping_id.tick) if dataset.mapping_id else tick
            bars = tuple(candle._to_bar() for candle in candles)
            key = f"{instrument.exchange}:{instrument.symbol}"
            assets.append(portfolio.Series(key, instrument.exchange, asset_tick, bars, revision._sessions()))
            inputs.append({"asset": key, "dataset": dataset.id, "source": dataset.source,
                           "calendar": revision.id, "calendar_digest": digest(revision.schedule),
                           "tick": asset_tick, "bars": len(bars), "input_digest": digest([asdict(bar) for bar in bars])})
        costs = tariff._schedule()
        try:
            output = portfolio.replay(assets, starts, ends, seconds, codes, costs, capital=capital)
        except (ValueError, ArithmeticError) as exc:
            raise ValidationError(str(exc)) from None
        specification = {
            "company": company.id, "scope": output["scope"], "starts": starts, "ends": ends,
            "interval_seconds": seconds, "capital": capital, "inputs": inputs, "tariff": tariff.id,
            "tariffs": [asdict(rule) for rule in costs.tariffs], "policy": output["policy"],
            "strategies": codes, "strategy_version": strategies.VERSION,
            "code_digests": {module.__name__.rsplit(".", 1)[-1]: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
                             for module in (portfolio, strategies, decision, eligibility, simulation, calendar)},
        }
        fingerprint = digest(specification)
        prior = self.search([("company_id", "=", company.id), ("fingerprint", "=", fingerprint)], limit=1)
        if prior:
            return prior
        return super(Portfolio, self.with_context({})).create([{
            **vals, "dataset_ids": [fields.Command.set(datasets.ids)], "company_id": company.id,
            "fingerprint": fingerprint, "trade_count": len(output["trades"]),
            "decision_count": len(output["decisions"]), "suspended": output["suspended"],
            "specification": json.dumps(specification, default=str, indent=2, sort_keys=True),
            "result": json.dumps(output, default=str, indent=2, sort_keys=True),
        }])

    def _parse_request(self, vals):
        try:
            starts, ends = fields.Date.to_date(vals["starts"]), fields.Date.to_date(vals["ends"])
            if not starts or not ends or ends > fields.Date.today() or not 0 <= (ends - starts).days <= 30:
                raise ValueError
            if any(not isinstance(vals[key], str) or not market_data.NUMBER.fullmatch(vals[key])
                   for key in ("capital", "tick")):
                raise ValueError
            if not isinstance(vals["strategy"], str) or vals["strategy"] not in dict(STRATEGIES):
                raise ValueError
            capital, tick = Decimal(vals["capital"]), Decimal(vals["tick"])
            if not 0 < capital <= 100_000_000 or not Decimal("0.000001") <= tick <= 10000:
                raise ValueError
            return starts, ends, capital, tick
        except (ValueError, TypeError, ArithmeticError):
            raise ValidationError(_("Use at most 31 historical dates, a listed strategy and valid capital and tick.")) from None

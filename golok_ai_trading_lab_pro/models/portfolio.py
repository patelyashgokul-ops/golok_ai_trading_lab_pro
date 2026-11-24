import hashlib
import json
from dataclasses import asdict, replace
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import (backtest, calendar, decision, eligibility, market_data, portfolio, replay_contract,
                        simulation, strategies, targets)


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
    target_policy = fields.Selection([("structure", "Completed market structure"), ("fixed_4r", "Fixed 4R benchmark")])
    fingerprint = fields.Char(required=True)
    trade_count = fields.Integer()
    decision_count = fields.Integer()
    suspended = fields.Boolean()
    specification = fields.Text(required=True)
    result = fields.Text(required=True)
    contract_fixture = fields.Boolean(readonly=True)

    _fingerprint = models.Constraint("UNIQUE(company_id,fingerprint)", "This portfolio already exists.")

    @api.model_create_multi
    def create(self, vals_list):
        return self._run_request(vals_list)

    def _run_request(self, vals_list, *, training=None, seal=None, contract_fixture=False):
        self.check_access("create")
        allowed = {"dataset_ids", "tariff_id", "starts", "ends", "capital", "tick", "strategy"}
        if len(vals_list) != 1 or not allowed <= set(vals_list[0]) <= allowed | {"target_policy"}:
            raise ValidationError(_("Supply one portfolio request with no generated fields."))
        vals = vals_list[0]
        target_policy = vals.get("target_policy", "structure")
        if target_policy not in ("structure", "fixed_4r"):
            raise ValidationError(_("Select a supported target policy."))
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
                or any(dataset.integrity_conflict or not dataset.calendar_id or not eligibility.evaluate(
                    dataset.origin, "synthetic_replay", quarantined=dataset.quarantined)[1]
                    for dataset in datasets)):
            raise ValidationError(_("Select calendar-bound eligible synthetic datasets with distinct instruments and one interval."))
        if contract_fixture and (training is not None or seal is not None or any(
                not dataset.fixture_version or not dataset.fixture_digest
                or dataset.calendar_id.verification != "fixture" for dataset in datasets)):
            raise AccessError(_("The historical timing test requires server-generated fixtures."))
        starts, ends, capital, tick = self._parse_request(vals)
        self.env["golok.lab.replay.guard"]._lock(datasets.instrument_id)
        overlap = [("company_id", "=", company.id), ("starts", "<=", ends), ("ends", ">=", starts),
                   ("dataset_ids.instrument_id", "in", datasets.instrument_id.ids)]
        reserved = self.env["golok.lab.holdout"].search(overlap)
        if reserved and (seal is None or reserved.ids != seal.ids):
            raise ValidationError(_("This instrument and date window is reserved for sealed evaluation."))
        if training is not None:
            training.check_access("read")
            previous_experiment = self.env["golok.lab.experiment"].search_count([
                *overlap[:-1], ("dataset_id.instrument_id", "in", datasets.instrument_id.ids)])
            left = datetime.combine(starts, time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
            right = datetime.combine(ends + timedelta(days=1), time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
            prior_snapshot = self.env["golok.lab.run"].sudo().search_count([
                ("company_id", "=", company.id), ("dataset_id.instrument_id", "in", datasets.instrument_id.ids),
                ("first_close", "<", right), ("last_close", ">=", left)], limit=1)
            if (not training or training.company_id != company or training.tariff_id != tariff
                    or set(training.dataset_ids.ids) != set(datasets.ids) or training.strategy != vals["strategy"]
                    or training.strategy == "all" or training.ends + timedelta(days=1) >= starts
                    or (training.target_policy or "fixed_4r") != target_policy
                    or Decimal(training.capital) != capital or Decimal(training.tick) != tick
                    or previous_experiment or prior_snapshot or self.search_count(overlap)):
                raise ValidationError(_("Select a matching earlier single-strategy replay and a previously unused holdout after an embargo."))
        code = vals["strategy"]
        codes = tuple(sorted(strategies.REGISTRY)) if code == "all" else (code,)
        seconds = market_data.INTERVALS[datasets[0].interval]
        opening = datetime.combine(starts, time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        ending = datetime.combine(ends + timedelta(days=1), time.min, calendar.IST).astimezone(timezone.utc).replace(tzinfo=None)
        assets, inputs, provenance = [], [], {}
        remaining = portfolio.MAX_BARS
        for dataset in datasets:
            candle_model = self.env["golok.lab.candle"]
            if seal is not None:
                candle_model = candle_model.sudo()
            candles = candle_model.search(
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
            sessions = revision._sessions()
            if contract_fixture:
                if not bars:
                    raise ValidationError(_("The fixture has no visible observations in the selected window."))
                bars = tuple(replace(bar, available_at=min(
                    bar.close_time + timedelta(minutes=1),
                    sessions[bar.close_time.astimezone(calendar.IST).date()].closing)) for bar in bars)
                asset = portfolio.Series(key, instrument.exchange, asset_tick, bars, sessions, origin="historical_contract")
                provenance[key] = replay_contract.Provenance(
                    "historical_intraday", dataset.interval, replay_contract.fingerprint(asset), "verified_publication",
                    True, True, True, True)
            else:
                asset = portfolio.Series(key, instrument.exchange, asset_tick, bars, sessions)
            assets.append(asset)
            inputs.append({"asset": key, "dataset": dataset.id, "source": dataset.source,
                           "calendar": revision.id, "calendar_digest": digest(revision.schedule),
                           "tick": asset_tick, "bars": len(bars), "input_digest": digest([asdict(bar) for bar in bars])})
        costs = tariff._schedule()
        specification = {
            "company": company.id, "scope": "SYNTHETIC_SOFTWARE_ONLY", "starts": starts, "ends": ends,
            "interval_seconds": seconds, "capital": capital, "inputs": inputs, "tariff": tariff.id,
            "tariffs": [asdict(rule) for rule in costs.tariffs], "policy": asdict(portfolio.PortfolioPolicy()),
            "strategies": codes, "strategy_version": strategies.VERSION,
            "target_policy": target_policy, "target_version": targets.VERSION,
            "code_digests": {module.__name__.rsplit(".", 1)[-1]: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
                             for module in (portfolio, strategies, decision, eligibility, simulation, calendar, targets)},
        }
        if contract_fixture:
            for item, dataset in zip(inputs, datasets):
                item["generated_fixture_digest"] = dataset.fixture_digest
            specification.update(scope="HISTORICAL_CONTRACT_FIXTURE_ONLY",
                                 publication_model="Authored fixture close plus one minute, bounded by session close",
                                 provenance={key: asdict(value) for key, value in provenance.items()})
            specification["code_digests"]["replay_contract"] = hashlib.sha256(
                Path(replay_contract.__file__).read_bytes()).hexdigest()
        fingerprint = digest(specification)
        if training is not None:
            try:
                portfolio._events(assets, starts, ends, seconds)
            except ValueError as exc:
                raise ValidationError(str(exc)) from None
            frozen = self.env["golok.lab.holdout"].with_context({}).sudo().create({
                "company_id": company.id, "training_id": training.id, "starts": starts, "ends": ends,
                "dataset_ids": [fields.Command.set(datasets.ids)], "fingerprint": fingerprint,
                "sealed_by": self.env.user.id, "specification": backtest.canonical(specification),
            })
            return self.env["golok.lab.holdout"].browse(frozen.id)
        if seal is not None and (not reserved or seal.fingerprint != fingerprint or seal.result_id):
            raise ValidationError(_("Holdout consumed or frozen inputs changed."))
        try:
            if contract_fixture:
                output = replay_contract.replay_fixture(assets, provenance, starts, ends, seconds, codes, costs,
                                                        capital=capital, target_policy=target_policy)
            else:
                output = portfolio.replay(assets, starts, ends, seconds, codes, costs, capital=capital,
                                          target_policy=target_policy)
        except (ValueError, ArithmeticError) as exc:
            raise ValidationError(str(exc)) from None
        prior = self.search([("company_id", "=", company.id), ("fingerprint", "=", fingerprint)], limit=1)
        if prior:
            return prior
        return super(Portfolio, self.with_context({})).create([{
            **vals, "dataset_ids": [fields.Command.set(datasets.ids)], "company_id": company.id,
            "fingerprint": fingerprint, "target_policy": target_policy, "trade_count": len(output["trades"]),
            "contract_fixture": contract_fixture,
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

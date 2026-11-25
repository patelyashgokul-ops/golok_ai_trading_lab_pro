import json
from datetime import timedelta
from decimal import Decimal

from odoo import fields, models
from odoo.exceptions import AccessError, ValidationError

from ..models.portfolio import STRATEGIES, digest
from ..services import backtest, performance, targets, walk_forward


class PortfolioWizard(models.TransientModel):
    _name = "golok.lab.portfolio.wizard"
    _description = "Run a synthetic portfolio replay"

    dataset_ids = fields.Many2many("golok.lab.dataset", string="Datasets", required=True)
    tariff_id = fields.Many2one("golok.lab.tariff", required=True)
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    capital = fields.Char(required=True, default="50000")
    tick = fields.Char(required=True, default="0.05", string="Unmapped Tick Size")
    strategy = fields.Selection(STRATEGIES, required=True, default="all")
    target_policy = fields.Selection(list(targets.POLICY_CHOICES), required=True, default="structure")
    training_id = fields.Many2one("golok.lab.portfolio", string="Training replay for sealing")
    training_sessions = fields.Integer(default=2)
    validation_sessions = fields.Integer(default=1)
    evaluation_sessions = fields.Integer(default=1)
    embargo_sessions = fields.Integer(default=1)
    expanding_window = fields.Boolean()
    calibrate_target = fields.Boolean(string="Fit a target cap on training observations")

    def action_seal(self):
        self.ensure_one()
        self.check_access("read")
        if not self.training_id:
            raise ValidationError("Select the frozen training replay.")
        seal = self.env["golok.lab.portfolio"]._run_request([{
            "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
            "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": self.strategy,
            "target_policy": self.target_policy,
        }], training=self.training_id)
        return {"type": "ir.actions.act_window", "res_model": seal._name, "res_id": seal.id,
                "views": [(False, "form")], "target": "current"}

    def action_run(self):
        self.ensure_one()
        self.check_access("read")
        record = self.env["golok.lab.portfolio"].create({
            "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
            "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": self.strategy,
            "target_policy": self.target_policy,
        })
        return {"type": "ir.actions.act_window", "res_model": record._name, "res_id": record.id,
                "views": [(False, "form")], "target": "current"}

    def action_run_timing_fixture(self):
        return self._run_alternate_replay(contract_fixture=True)

    def action_run_authorized_history(self):
        return self._run_alternate_replay(historical=True)

    def _run_alternate_replay(self, **mode):
        self.ensure_one()
        self.check_access("read")
        record = self.env["golok.lab.portfolio"]._run_request([{
            "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
            "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": self.strategy,
            "target_policy": self.target_policy,
        }], **mode)
        return {"type": "ir.actions.act_window", "res_model": record._name, "res_id": record.id,
                "views": [(False, "form")], "target": "current"}

    def action_compare(self):
        self.ensure_one()
        self.check_access("read")
        records = self.env["golok.lab.portfolio"]
        for code, _name in STRATEGIES:
            if code != "all":
                records |= records.create({
                    "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
                    "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": code,
                    "target_policy": self.target_policy,
                })
        return {"type": "ir.actions.act_window", "name": "Synthetic Strategy Comparison",
                "res_model": records._name, "domain": [("id", "in", records.ids)],
                "views": [(False, "list"), (False, "form")], "target": "current"}

    def action_walk_forward(self):
        self.ensure_one()
        self.check_access("read")
        duration = (self.ends - self.starts).days
        if not 3 <= duration <= 8:
            raise ValidationError("Select four to nine calendar dates with explicit session coverage.")
        # Each validation day follows a two-date fit and a one-date embargo.
        folds = []
        for offset in range(duration - 2):
            start = self.starts + timedelta(days=offset)
            inputs = {"dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id,
                      "capital": self.capital, "tick": self.tick, "target_policy": self.target_policy}
            portfolios = self.env["golok.lab.portfolio"]
            scored = []
            for code, _label in STRATEGIES:
                if code == "all":
                    continue
                training = portfolios.create({**inputs, "starts": start, "ends": start + timedelta(days=1),
                                              "strategy": code})
                if training.trade_count:
                    scored.append((Decimal(json.loads(training.result)["net"]), code, training.id))
            if scored:
                # Ties use strategy code; validation observations never enter selection.
                _, selected, _ = min(scored, key=lambda entry: (-entry[0], entry[1]))
                validation = start + timedelta(days=3)
                folds.append(portfolios.create({**inputs, "starts": validation, "ends": validation,
                                                "strategy": selected}).id)
        return {"type": "ir.actions.act_window", "name": "Walk-forward Validation Replays",
                "res_model": "golok.lab.portfolio", "domain": [("id", "in", folds)],
                "views": [(False, "list"), (False, "form")], "target": "current"}

    def action_experiment(self):
        self.ensure_one()
        self.check_access("read")
        datasets = self.dataset_ids
        datasets.check_access("read")
        company = self.env.company
        if (not self.env.user.has_group("golok_ai_trading_lab_pro.group_analyst") or not datasets
                or len(datasets) > 16 or any(data.company_id != company or data.origin != "synthetic"
                                            or not data.calendar_id for data in datasets)):
            raise AccessError("Use active-company, calendar-bound synthetic datasets.")
        if not self.starts or not self.ends or not 0 <= (self.ends - self.starts).days <= 30:
            raise ValidationError("Use up to 31 calendar dates.")
        requested = [self.starts + timedelta(days=offset) for offset in range((self.ends - self.starts).days + 1)]
        schedules = [data.calendar_id._sessions() for data in datasets]
        if any(not all(day in schedule for day in requested) for schedule in schedules):
            raise ValidationError("Each date needs explicit calendar coverage.")
        days = [day for day in requested if all(schedule[day].kind == "regular" for schedule in schedules)]
        try:
            partitions = list(walk_forward.folds(
                days, training=self.training_sessions, validation=self.validation_sessions,
                evaluation=self.evaluation_sessions, embargo=self.embargo_sessions, expanding=self.expanding_window))
            if not 1 <= len(partitions) <= 6:
                raise ValueError("Select a window producing one to six bounded folds.")
        except ValueError as exc:
            raise ValidationError(str(exc)) from None
        self.env["golok.lab.replay.guard"]._lock(datasets.instrument_id)
        if self.env["golok.lab.holdout"].search_count([
                ("company_id", "=", company.id), ("starts", "<=", self.ends), ("ends", ">=", self.starts),
                ("dataset_ids.instrument_id", "in", datasets.instrument_id.ids)], limit=1):
            raise ValidationError("This experiment overlaps a sealed holdout.")
        request = {"dataset_ids": sorted(datasets.ids), "tariff_id": self.tariff_id.id, "capital": self.capital,
                   "tick": self.tick, "target_policy": self.target_policy}
        portfolios = self.env["golok.lab.portfolio"]
        codes = sorted(code for code, _label in STRATEGIES if code != "all")
        grid = self.target_policy == targets.JOINT_POLICY
        calibration = self.calibrate_target
        if calibration and not grid:
            raise ValidationError("Select the experimental causal policy to fit a target cap.")
        trial_policies = targets.POLICIES if grid else (self.target_policy,)
        version = (walk_forward.CALIBRATION_VERSION if calibration else
                   walk_forward.GRID_VERSION if grid else walk_forward.VERSION)
        results = []

        def replay(window, code, policy, cap=None):
            vals = {**request, "starts": window[0], "ends": window[-1], "strategy": code, "target_policy": policy}
            portfolio = portfolios._run_request([vals], target_cap=cap) if cap is not None else portfolios.create(vals)
            metrics = performance.summarize(json.loads(portfolio.result))
            result = {"strategy": code, "fingerprint": portfolio.fingerprint, "portfolio": portfolio.id, "metrics": metrics}
            if grid:
                result["target_policy"] = policy
            if cap is not None:
                result["target_cap"] = cap
            return result

        for windows in partitions:
            trials = [replay(windows["training"], code, policy) for code in codes for policy in trial_policies]
            fitted = []
            if calibration:
                for baseline in [trial for trial in trials if trial["target_policy"] == "fixed_4r"]:
                    baseline_run = portfolios.browse(baseline["portfolio"])
                    fit = performance.train_target_cap(json.loads(baseline_run.result), baseline_run._frozen_mark_series())
                    fit.update(strategy=baseline["strategy"], baseline_fingerprint=baseline["fingerprint"])
                    if fit["fraction"] is not None:
                        fit["trial"] = replay(windows["training"], fit["strategy"], "atr_barrier", fit["fraction"])
                    fitted.append(fit)
            eligible = trials + [fit["trial"] for fit in fitted if "trial" in fit]
            selected = walk_forward.choose_training_trial(
                [{**trial, "target_policy": trial.get("target_policy", self.target_policy)} for trial in eligible])
            fold = {"windows": windows, "training_trials": trials, "status": "INSUFFICIENT_TRAINING"}
            if calibration:
                fold["target_calibration"] = fitted
            if selected:
                code, policy = selected["strategy"], selected["target_policy"]
                cap = selected.get("target_cap")
                validation = replay(windows["validation"], code, policy, cap)
                fold.update(selected=code, validation=validation, status="VALIDATION_VETO")
                if grid:
                    fold["selected_target_policy"] = policy
                if cap is not None:
                    fold["selected_target_cap"] = cap
                if walk_forward.rank_summary(validation["metrics"]) is not None:
                    fold.update(evaluation=replay(windows["evaluation"], code, policy, cap), status="EVALUATED")
            results.append(fold)
        report = {"version": version, "scope": "SYNTHETIC_SOFTWARE_ONLY", "folds": results,
                  "selection": "Positive net expectancy with at least two trades, then lower closed-trade drawdown, trade count and fees",
                  "parameters": {**request, "training_sessions": self.training_sessions, "validation_sessions": self.validation_sessions,
                                 "evaluation_sessions": self.evaluation_sessions, "embargo_sessions": self.embargo_sessions,
                                 "expanding": self.expanding_window}}
        key = digest(report)
        stored = self.env["golok.lab.walk.experiment"]
        record = stored.search([("company_id", "=", company.id), ("fingerprint", "=", key)], limit=1)
        if not record:
            record = stored.with_context({}).sudo().create({
                "company_id": company.id, "fingerprint": key, "version": version,
                "fold_count": len(results), "report": backtest.canonical(report),
            })
        return {"type": "ir.actions.act_window", "res_model": stored._name, "res_id": record.id,
                "views": [(False, "form")], "target": "current"}

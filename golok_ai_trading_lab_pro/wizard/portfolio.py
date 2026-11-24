import json
from datetime import timedelta
from decimal import Decimal

from odoo import fields, models
from odoo.exceptions import ValidationError

from ..models.portfolio import STRATEGIES


class PortfolioWizard(models.TransientModel):
    _name = "golok.lab.portfolio.wizard"
    _description = "Run a synthetic portfolio replay"

    dataset_ids = fields.Many2many("golok.lab.dataset", string="Synthetic Datasets", required=True)
    tariff_id = fields.Many2one("golok.lab.tariff", required=True)
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    capital = fields.Char(required=True, default="50000")
    tick = fields.Char(required=True, default="0.05", string="Unmapped Tick Size")
    strategy = fields.Selection(STRATEGIES, required=True, default="all")
    training_id = fields.Many2one("golok.lab.portfolio", string="Training replay for sealing")

    def action_seal(self):
        self.ensure_one()
        self.check_access("read")
        if not self.training_id:
            raise ValidationError("Select the frozen training replay.")
        seal = self.env["golok.lab.portfolio"]._run_request([{
            "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
            "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": self.strategy,
        }], training=self.training_id)
        return {"type": "ir.actions.act_window", "res_model": seal._name, "res_id": seal.id,
                "views": [(False, "form")], "target": "current"}

    def action_run(self):
        self.ensure_one()
        self.check_access("read")
        record = self.env["golok.lab.portfolio"].create({
            "dataset_ids": self.dataset_ids.ids, "tariff_id": self.tariff_id.id, "starts": self.starts,
            "ends": self.ends, "capital": self.capital, "tick": self.tick, "strategy": self.strategy,
        })
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
                      "capital": self.capital, "tick": self.tick}
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

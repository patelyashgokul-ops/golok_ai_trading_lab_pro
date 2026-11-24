from odoo import fields, models

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

from odoo import fields, models


class ExperimentWizard(models.TransientModel):
    _name = "golok.lab.experiment.wizard"
    _description = "Run a synthetic historical experiment"

    dataset_id = fields.Many2one("golok.lab.dataset", required=True)
    tariff_id = fields.Many2one("golok.lab.tariff", required=True)
    strategy_id = fields.Many2one("golok.lab.strategy", required=True,
                                  default=lambda self: self.env.ref("golok_ai_trading_lab_pro.strategy_st01_p03"))
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    capital = fields.Char(required=True, default="50000")
    tick = fields.Char(required=True, default="0.05")

    def action_run(self):
        self.ensure_one()
        self.check_access("read")
        experiment = self.env["golok.lab.experiment"].create({
            "dataset_id": self.dataset_id.id, "tariff_id": self.tariff_id.id, "strategy_id": self.strategy_id.id,
            "starts": self.starts, "ends": self.ends, "capital": self.capital, "tick": self.tick,
        })
        return {"type": "ir.actions.act_window", "res_model": experiment._name,
                "res_id": experiment.id, "views": [(False, "form")], "target": "current"}

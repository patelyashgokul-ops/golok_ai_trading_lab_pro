from odoo import fields, models


class PaperReplayWizard(models.TransientModel):
    _name = "golok.lab.paper.wizard"
    _description = "Post a historical virtual replay"

    account_id = fields.Many2one("golok.lab.paper.account", required=True)
    experiment_id = fields.Many2one("golok.lab.experiment", required=True)

    def action_post(self):
        self.ensure_one()
        self.check_access("read")
        batch = self.account_id._post_replay(self.experiment_id)
        return {"type": "ir.actions.act_window", "res_model": batch._name,
                "res_id": batch.id, "views": [(False, "form")], "target": "current"}

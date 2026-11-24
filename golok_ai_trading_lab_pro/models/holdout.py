from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError


class ReplayGuard(models.Model):
    _name = "golok.lab.replay.guard"
    _description = "Serialize portfolio evaluation and holdout reservation"
    _log_access = False

    instrument_id = fields.Many2one("golok.lab.instrument", required=True, ondelete="restrict")
    _identity = models.Constraint("UNIQUE(instrument_id)", "One replay guard per instrument.")

    @api.model
    def _lock(self, instruments):
        for instrument_id in sorted(instruments.ids):
            self.env.cr.execute("""
                INSERT INTO golok_lab_replay_guard (instrument_id) VALUES (%s)
                ON CONFLICT (instrument_id) DO UPDATE SET instrument_id = EXCLUDED.instrument_id
            """, (instrument_id,))


class Holdout(models.Model):
    _name = "golok.lab.holdout"
    _description = "Sealed synthetic portfolio evaluation"
    _rec_name = "fingerprint"
    _order = "id desc"

    company_id = fields.Many2one("res.company", required=True, index=True)
    training_id = fields.Many2one("golok.lab.portfolio", required=True, ondelete="restrict")
    dataset_ids = fields.Many2many("golok.lab.dataset")
    starts = fields.Date(required=True)
    ends = fields.Date(required=True)
    fingerprint = fields.Char(required=True)
    specification = fields.Text(required=True)
    sealed_by = fields.Many2one("res.users", required=True)
    consumed_by = fields.Many2one("res.users")
    consumed_at = fields.Datetime()
    result_id = fields.Many2one("golok.lab.portfolio", ondelete="restrict")

    def action_consume(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_risk"):
            raise AccessError("A risk manager in the active company must authorize final evaluation.")
        self.env.cr.execute("SELECT id FROM golok_lab_holdout WHERE id = %s FOR UPDATE", (self.id,))
        self.invalidate_recordset()
        if self.result_id:
            raise ValidationError("This holdout has already been consumed.")
        training = self.training_id
        result = self.env["golok.lab.portfolio"]._run_request([{
            "dataset_ids": self.dataset_ids.ids, "starts": self.starts, "ends": self.ends,
            "strategy": training.strategy, "tick": training.tick, "capital": training.capital,
            "tariff_id": training.tariff_id.id,
        }], seal=self)
        self.sudo().write({"result_id": result.id, "consumed_by": self.env.user.id, "consumed_at": fields.Datetime.now()})
        return {"type": "ir.actions.act_window", "res_model": result._name, "res_id": result.id,
                "views": [(False, "form")], "target": "current"}

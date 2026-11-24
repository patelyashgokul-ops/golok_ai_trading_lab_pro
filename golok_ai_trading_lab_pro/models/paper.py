import json

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import paper


class PaperAccount(models.Model):
    _name = "golok.lab.paper.account"
    _description = "Virtual historical replay account"
    _check_company_auto = True

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, index=True)
    initial_deposit = fields.Char(required=True, default="50000")
    opening_paise = fields.Integer(readonly=True)
    available_paise = fields.Integer(readonly=True)
    posted_end = fields.Date(readonly=True)

    _cash = models.Constraint("CHECK (opening_paise > 0 AND available_paise >= 0)", "Virtual cash cannot be negative.")

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        prepared = []
        for vals in vals_list:
            if set(vals) - {"name", "initial_deposit"} or not vals.get("name"):
                raise ValidationError(_("Supply an account name and an optional virtual opening deposit."))
            try:
                deposit = vals.get("initial_deposit", "50000")
                if not isinstance(deposit, str) or len(deposit) > 16:
                    raise ValueError("Enter a decimal virtual opening deposit.")
                opening = paper.paise(deposit)
                if opening <= 0:
                    raise ValueError("Virtual cash must start positive.")
            except ValueError as exc:
                raise ValidationError(str(exc)) from None
            prepared.append({
                "name": vals["name"], "company_id": self.env.company.id, "initial_deposit": deposit,
                "opening_paise": opening, "available_paise": opening,
            })
        return super(PaperAccount, self.with_context({})).create(prepared)

    def _post_replay(self, experiment):
        self.ensure_one()
        experiment.ensure_one()
        self.check_access("read")
        experiment.check_access("read")
        if not self.env.user.has_group("golok_ai_trading_lab_pro.group_risk"):
            raise AccessError(_("Only Trading Risk Managers may post a historical replay."))
        if self.company_id != self.env.company or experiment.company_id != self.company_id:
            raise AccessError(_("Use records from the active company."))
        batches = self.env["golok.lab.paper.batch"]
        with self.env.cr.savepoint():
            self.env.cr.execute("SELECT id FROM golok_lab_paper_account WHERE id = %s FOR UPDATE", [self.id])
            self.invalidate_recordset(["available_paise", "posted_end"])
            existing = batches.search([("account_id", "=", self.id), ("experiment_id", "=", experiment.id)], limit=1)
            if existing:
                return existing
            if (experiment.status != "completed" or not experiment.trade_count or experiment.dataset_id.origin != "synthetic"
                    or experiment.dataset_id.quarantined):
                raise ValidationError(_("Use a completed, non-quarantined synthetic replay with trades."))
            if self.posted_end and experiment.starts <= self.posted_end:
                raise ValidationError(_("This experiment overlaps or precedes posted account history."))
            try:
                if paper.paise(experiment.capital) != self.available_paise:
                    raise ValueError("Frozen starting capital does not match available virtual cash.")
                outcome = json.loads(experiment.result)
                available, lines = paper.postings(outcome["trades"], self.available_paise)
            except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
                raise ValidationError(_("The synthetic replay cannot be reconciled: %s", str(exc))) from None
            batch = batches.with_context({}).sudo().create({
                "company_id": self.company_id.id, "account_id": self.id, "experiment_id": experiment.id,
                "before_paise": self.available_paise, "after_paise": available,
            })
            self.env["golok.lab.paper.event"].with_context({}).sudo().create([
                dict(event, batch_id=batch.id) for event in lines
            ])
            self.with_context({}).sudo().write({"available_paise": available, "posted_end": experiment.ends})
            return batches.browse(batch.id)


class PaperBatch(models.Model):
    _name = "golok.lab.paper.batch"
    _description = "Posted historical replay"
    _rec_name = "experiment_id"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", required=True, index=True)
    account_id = fields.Many2one("golok.lab.paper.account", required=True, ondelete="restrict", check_company=True)
    experiment_id = fields.Many2one("golok.lab.experiment", required=True, ondelete="restrict", check_company=True)
    before_paise = fields.Integer(required=True)
    after_paise = fields.Integer(required=True)
    event_ids = fields.One2many("golok.lab.paper.event", "batch_id")

    _identity = models.Constraint("UNIQUE(account_id,experiment_id)", "This replay was already posted.")
    _cash = models.Constraint("CHECK (before_paise >= 0 AND after_paise >= 0)", "Batch cash cannot be negative.")


class PaperEvent(models.Model):
    _name = "golok.lab.paper.event"
    _description = "Immutable virtual ledger event"
    _order = "id"

    batch_id = fields.Many2one("golok.lab.paper.batch", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one(related="batch_id.company_id", store=True, index=True)
    sequence = fields.Integer(required=True)
    kind = fields.Selection([("reserve", "Reserve virtual cash"), ("buy_fill", "Simulated buy"),
                             ("sell_fill", "Simulated close")], required=True)
    cash_delta = fields.Integer()
    reserved_delta = fields.Integer()
    quantity_delta = fields.Integer()
    fee = fields.Integer()
    realized = fields.Integer()
    available_after = fields.Integer()
    reserved_after = fields.Integer()

    _identity = models.Constraint("UNIQUE(batch_id,sequence,kind)", "Duplicate virtual fill or reservation.")
    _nonnegative = models.Constraint("CHECK (available_after >= 0 AND reserved_after >= 0 AND fee >= 0)", "Invalid virtual balance.")

from decimal import Decimal

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import paper, simulation


class FixturePaperAccount(models.Model):
    _name = "golok.lab.fixture.account"
    _description = "Prospective fixture-only paper account"
    _order = "id desc"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    currency_id = fields.Many2one("res.currency", required=True, readonly=True)
    mode = fields.Selection([("fixture", "Prospective fixture simulation")], required=True)
    opening = fields.Integer(readonly=True, string="Opening Capital (paise)")
    available = fields.Integer(readonly=True, string="Available Cash (paise)")
    reserved = fields.Integer(readonly=True, string="Reserved Cash (paise)")
    position_cost = fields.Integer(readonly=True, string="Open Cost (paise)")
    realized = fields.Integer(readonly=True, string="Realized Net (paise)")
    planned_risk = fields.Integer(readonly=True, string="Planned Risk (paise)")
    daily_open = fields.Integer(readonly=True)
    daily_realized = fields.Integer(readonly=True)
    entries = fields.Integer(readonly=True)
    loss_streak = fields.Integer(readonly=True)
    state = fields.Selection([("active", "Active"), ("paused", "Paused"), ("risk", "Risk suspension")], required=True)
    day = fields.Date(readonly=True)
    order_ids = fields.One2many("golok.lab.fixture.order", "account_id")
    journal_ids = fields.One2many("golok.lab.fixture.journal", "account_id")
    fixture_stage = fields.Selection([("pending", "Pending entry"), ("open", "Open")], compute="_compute_fixture_stage")
    scenario = fields.Selection([("target", "Target"), ("ambiguous", "Stop and target touched"),
                                 ("missing", "Missing exit observation")], required=True, default="target")
    tariff_id = fields.Many2one("golok.lab.tariff", required=True, ondelete="restrict")

    _cash = models.Constraint("CHECK(available >= 0 AND reserved >= 0 AND position_cost >= 0 AND planned_risk >= 0)",
                              "Invalid fixture cash or risk balance.")

    @api.depends("order_ids.state")
    def _compute_fixture_stage(self):
        for account in self:
            account.fixture_stage = account.order_ids.filtered(lambda item: item.state in ("pending", "open"))[:1].state

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        if any(set(vals) - {"name", "scenario", "tariff_id"} for vals in vals_list):
            raise ValidationError(_("Supply only a fixture account name, scenario and hypothetical tariff."))
        for vals in vals_list:
            tariff = self.env["golok.lab.tariff"].search([("id", "=", vals.get("tariff_id")),
                                                          ("company_id", "=", self.env.company.id)], limit=1)
            if not tariff:
                raise AccessError(_("Select a tariff from the active company."))
        return super(FixturePaperAccount, self.with_context({})).create([
            {**vals, "company_id": self.env.company.id, "mode": "fixture", "opening": 5000000,
             "available": 5000000, "daily_open": 5000000, "state": "active",
             "currency_id": self.env.ref("base.INR").id} for vals in vals_list
        ])

    def _lock(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_risk"):
            raise AccessError(_("An active-company risk manager is required."))
        self.env.cr.execute("SELECT id FROM golok_lab_fixture_account WHERE id=%s FOR UPDATE", (self.id,))
        self.invalidate_recordset()

    def _post(self, kind, *, order=None, available=0, reserved=0, cost=0, realized=0, risk=0, **settings):
        names = {"available": available, "reserved": reserved, "position_cost": cost,
                 "realized": realized, "planned_risk": risk}
        updated = {name: self[name] + delta for name, delta in names.items()}
        if (min(updated[name] for name in ("available", "reserved", "position_cost", "planned_risk")) < 0
                or any(abs(value) > paper.MAX_CASH for value in updated.values())
                or updated["available"] + updated["reserved"] + updated["position_cost"] != self.opening + updated["realized"]):
            raise ValidationError(_("The fixture journal does not reconcile."))
        self.sudo().write({**updated, **settings})
        self.env["golok.lab.fixture.journal"].with_context({}).sudo().create({
            "account_id": self.id, "company_id": self.company_id.id, "order_id": order.id if order else False,
            "kind": kind, "user_id": self.env.uid, "delta_cash": available, "delta_reserved": reserved,
            "delta_cost": cost, "delta_net": realized, "cash_after": updated["available"],
            "reserved_after": updated["reserved"], "position_after": updated["position_cost"],
        })
        self.invalidate_recordset()

    def action_pause(self):
        self._lock()
        if self.state != "active":
            return
        pending = self.order_ids.filtered(lambda item: item.state == "pending")
        for order in pending:
            self._cancel(order)
        self._post("paused", state="paused")

    def action_resume(self):
        self._lock()
        if self.state != "paused" or self.loss_streak >= 2 or self.order_ids.filtered(
                lambda item: item.state in ("open", "unresolved")):
            raise ValidationError(_("Resolve open risk or retain the suspension before resuming."))
        self._post("resumed", state="active")

    def _cancel(self, order):
        order.sudo().write({"state": "cancelled"})
        self._post("cancelled", order=order, available=order.reserved, reserved=-order.reserved, risk=-order.risk)

    def action_reserve_fixture(self):
        self._lock()
        if self.state != "active" or self.order_ids.filtered(lambda item: item.state in ("pending", "open", "unresolved")):
            raise ValidationError(_("The fixture account has an active order or is suspended."))
        day = fields.Date.context_today(self.with_context(tz="Asia/Kolkata"))
        if self.day != day:
            self.sudo().write({"day": day, "daily_open": self.available, "daily_realized": 0, "entries": 0})
            self.invalidate_recordset()
        if self.entries >= 3 or self.loss_streak >= 2 or self.daily_realized * 100 <= -self.daily_open:
            raise ValidationError(_("The fixture exceeded a daily or consecutive-loss risk limit."))
        # Known authored test order. Its fixed target is an explicit execution fixture.
        entry, stop, target, tick = map(Decimal, ("100", "98", "108", ".05"))
        costs = self.tariff_id._schedule()
        capital = Decimal(min(self.available, self.daily_open)) / 100
        try:
            policy = simulation.RiskPolicy(capital=capital)
            size = simulation.size_long(entry, stop, target, tick, 4000, day, "NSE", costs, policy)
            if not size.quantity:
                raise ValueError(size.reason)
            buy_fee = paper.paise(sum(costs.fees(day, "NSE", "buy", entry, size.quantity).values()))
            reserved = paper.paise(entry * size.quantity) + buy_fee
            risk = paper.paise(size.loss)
            if risk + self.planned_risk - min(self.daily_realized, 0) > self.daily_open // 100:
                raise ValueError("Aggregate daily planned risk exceeds the remaining budget.")
            exit_price = Decimal("97") if self.scenario == "ambiguous" else target
            exit_fee = paper.paise(sum(costs.fees(day, "NSE", "sell", exit_price, size.quantity).values()))
        except (ValueError, ArithmeticError) as exc:
            raise ValidationError(_("The fixture order failed risk or cost checks: %s", str(exc))) from None
        order = self.env["golok.lab.fixture.order"].with_context({}).sudo().create({
            "account_id": self.id, "company_id": self.company_id.id, "state": "pending", "scenario": self.scenario,
            "quantity": size.quantity, "risk": risk, "reserved": reserved,
            "entry_fee": buy_fee, "exit_fee": exit_fee, "exit_paise": paper.paise(exit_price),
        })
        self._post("reserved", order=order, available=-reserved, reserved=reserved, risk=risk)

    def action_open_fixture(self):
        self._advance_fixture("pending")

    def action_close_fixture(self):
        self._advance_fixture("open")

    def _advance_fixture(self, expected):
        self._lock()
        order = self.order_ids.filtered(lambda item: item.state == expected)[:1]
        if not order:
            return
        if order.state == "pending":
            today = fields.Date.context_today(self.with_context(tz="Asia/Kolkata"))
            if today != self.day or self.state != "active":
                self._cancel(order)
                return
            order.sudo().write({"state": "open", "entry_observed_at": fields.Datetime.now()})
            self._post("opened", order=order, reserved=-order.reserved, cost=order.reserved, entries=self.entries + 1)
        elif order.scenario == "missing":
            order.sudo().write({"state": "unresolved", "exit_observed_at": fields.Datetime.now()})
            self._post("unresolved", order=order, state="risk")
        else:
            proceeds = order.exit_paise * order.quantity - order.exit_fee
            net = proceeds - order.reserved
            streak = self.loss_streak + 1 if net < 0 else 0
            daily = self.daily_realized + net
            order.sudo().write({"state": "closed", "exit_observed_at": fields.Datetime.now(), "net": net})
            self._post("closed", order=order, available=proceeds, cost=-order.reserved, realized=net,
                       risk=-order.risk, daily_realized=daily, loss_streak=streak,
                       state="risk" if streak >= 2 or daily * 100 <= -self.daily_open else self.state)


class FixturePaperOrder(models.Model):
    _name = "golok.lab.fixture.order"
    _description = "Authored prospective simulation order and position"
    _order = "id desc"

    account_id = fields.Many2one("golok.lab.fixture.account", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    scenario = fields.Char(required=True)
    state = fields.Selection([("pending", "Pending entry"), ("open", "Open"), ("closed", "Closed"),
                              ("cancelled", "Cancelled"), ("unresolved", "Reconciliation required")], required=True)
    quantity = fields.Integer(required=True)
    risk = fields.Integer(required=True)
    reserved = fields.Integer(required=True)
    entry_fee = fields.Integer()
    exit_fee = fields.Integer()
    exit_paise = fields.Integer()
    entry_observed_at = fields.Datetime()
    exit_observed_at = fields.Datetime()
    net = fields.Integer()


class FixturePaperJournal(models.Model):
    _name = "golok.lab.fixture.journal"
    _description = "Append-only prospective fixture journal"
    _order = "id"

    account_id = fields.Many2one("golok.lab.fixture.account", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    order_id = fields.Many2one("golok.lab.fixture.order", ondelete="restrict")
    user_id = fields.Many2one("res.users", required=True, ondelete="restrict")
    kind = fields.Selection([(key, key.title()) for key in
                             ("reserved", "opened", "closed", "unresolved", "cancelled", "paused", "resumed")],
                            required=True)
    delta_cash = fields.Integer()
    delta_reserved = fields.Integer()
    delta_cost = fields.Integer()
    delta_net = fields.Integer()
    cash_after = fields.Integer()
    reserved_after = fields.Integer()
    position_after = fields.Integer()

    _event_once = models.Constraint("UNIQUE(order_id,kind)", "This fixture order event has already been recorded.")

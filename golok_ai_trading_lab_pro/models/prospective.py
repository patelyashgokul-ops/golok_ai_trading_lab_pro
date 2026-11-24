from datetime import timedelta, timezone
from decimal import Decimal

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Domain

from .lab import _input_digest
from ..services import fixture_execution, market_data, paper, simulation, strategies


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
    remaining_daily_risk = fields.Integer(compute="_compute_remaining_daily_risk", string="Remaining Daily Risk (paise)")
    state = fields.Selection([("active", "Active"), ("paused", "Paused"), ("risk", "Risk suspension")], required=True)
    day = fields.Date(readonly=True)
    order_ids = fields.One2many("golok.lab.fixture.order", "account_id")
    journal_ids = fields.One2many("golok.lab.fixture.journal", "account_id")
    fixture_stage = fields.Selection([("pending", "Pending entry"), ("open", "Open")], compute="_compute_fixture_stage")
    scenario = fields.Selection([("target", "Target"), ("ambiguous", "Stop and target touched"),
                                 ("severe_gap", "Gap beyond daily risk"),
                                 ("missing", "Missing exit observation")], required=True, default="target")
    tariff_id = fields.Many2one("golok.lab.tariff", required=True, ondelete="restrict")
    bound_watch_ids = fields.One2many("golok.lab.session.watch", "paper_account_id")
    watch_ids = fields.Many2many("golok.lab.session.watch", compute="_compute_watches", readonly=False,
                                string="Automated Fixture Research Schedules")
    strategy = fields.Selection([(code, item.name) for code, item in strategies.REGISTRY.items()], default="ST-01")
    target_policy = fields.Selection([("structure", "Completed market structure"), ("fixed_4r", "Fixed 4R benchmark")],
                                     default="structure")

    _cash = models.Constraint("CHECK(available >= 0 AND reserved >= 0 AND position_cost >= 0 AND planned_risk >= 0)",
                              "Invalid fixture cash or risk balance.")

    @api.depends("order_ids.state")
    def _compute_fixture_stage(self):
        for account in self:
            account.fixture_stage = account.order_ids.filtered(lambda item: item.state in ("pending", "open"))[:1].state

    @api.depends("bound_watch_ids")
    def _compute_watches(self):
        for account in self:
            account.watch_ids = account.bound_watch_ids

    @api.depends("daily_open", "daily_realized", "planned_risk", "state")
    def _compute_remaining_daily_risk(self):
        for account in self:
            account.remaining_daily_risk = max(0, account.daily_open // 100 + min(0, account.daily_realized)
                                               - account.planned_risk) if account.state == "active" else 0

    @api.model_create_multi
    def create(self, vals_list):
        self.check_access("create")
        allowed = {"name", "scenario", "tariff_id", "watch_ids", "strategy", "target_policy"}
        if any(set(vals) - allowed for vals in vals_list):
            raise ValidationError(_("Supply only fixture account configuration."))
        prepared, bindings = [], []
        for vals in vals_list:
            vals = dict(vals)
            tariff = self.env["golok.lab.tariff"].search([("id", "=", vals.get("tariff_id")),
                                                          ("company_id", "=", self.env.company.id)], limit=1)
            if not tariff:
                raise AccessError(_("Select a tariff from the active company."))
            watches = self._lock_watch_binding(vals.pop("watch_ids", []))
            if watches and vals.get("scenario", "target") != "target":
                raise ValidationError(_("Scripted scenarios are only available on unbound fixture accounts."))
            if any(watch in existing for existing in bindings for watch in watches):
                raise ValidationError(_("A fixture research schedule may belong to only one paper account."))
            bindings.append(watches)
            prepared.append({**vals, "company_id": self.env.company.id, "mode": "fixture", "opening": 5000000,
                             "available": 5000000, "daily_open": 5000000, "state": "active",
                             "currency_id": self.env.ref("base.INR").id})
        accounts = super(FixturePaperAccount, self.with_context({})).create(prepared)
        for account, watches in zip(accounts, bindings):
            watches.sudo().write({"paper_account_id": account.id})
        return accounts

    def _lock_watch_binding(self, commands):
        watches = self.env["golok.lab.session.watch"]
        if not commands:
            return watches
        if (not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin")
                or not isinstance(commands, (list, tuple)) or len(commands) > 16):
            raise AccessError(_("A schedule administrator must bind fixture watches."))
        ids = set()
        for command in commands:
            if not isinstance(command, (list, tuple)) or len(command) != 3:
                raise ValidationError(_("Select existing fixture watches."))
            operation, key, value = command
            if operation == fields.Command.SET and isinstance(value, (list, tuple)) and len(value) <= 16:
                selected = value
            elif operation == fields.Command.LINK:
                selected = [key]
            else:
                raise ValidationError(_("Select existing fixture watches."))
            if any(type(item) is not int or item <= 0 for item in selected):
                raise ValidationError(_("Select existing fixture watches."))
            ids.update(selected)
        if len(ids) > 16:
            raise ValidationError(_("Use up to 16 fixture watches."))
        records = watches.search([("id", "in", sorted(ids)), ("company_id", "=", self.env.company.id)])
        if set(records.ids) != ids:
            raise AccessError(_("Select fixture watches in the active company."))
        if ids:
            self.env.cr.execute("SELECT id FROM golok_lab_session_watch WHERE id IN %s ORDER BY id FOR UPDATE", (tuple(ids),))
            records.invalidate_recordset(["paper_account_id"])
            if records.mapped("paper_account_id"):
                raise ValidationError(_("A fixture research schedule may belong to only one paper account."))
        return records

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

    def _cancel(self, order, reason=None):
        order.sudo().write({"state": "cancelled", "exit_reason": reason})
        self._post("cancelled", order=order, available=order.reserved, reserved=-order.reserved, risk=-order.risk)

    def action_reserve_fixture(self):
        self._lock()
        if self.sudo().bound_watch_ids:
            raise ValidationError(_("This account uses the automatic fixture schedule."))
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
            exit_price = {"ambiguous": Decimal("97"), "severe_gap": Decimal("80")}.get(self.scenario, target)
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
        if self.sudo().bound_watch_ids:
            raise ValidationError(_("This account uses the automatic fixture schedule."))
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
            self._close_position(order, order.exit_paise, order.exit_fee, fields.Datetime.now())

    def _close_position(self, order, price, fee, observed, *, candle=None, reason=None):
        proceeds = price * order.quantity - fee
        net = proceeds - order.reserved
        streak = self.loss_streak + 1 if net < 0 else 0
        daily = self.daily_realized + net
        values = {"state": "closed", "exit_observed_at": observed, "net": net}
        if candle:
            values.update(exit_candle_id=candle.id, exit_paise=price, exit_fee=fee, exit_reason=reason)
        order.sudo().write(values)
        self._post("closed", order=order, available=proceeds, cost=-order.reserved, realized=net,
                   risk=-order.risk, daily_realized=daily, loss_streak=streak,
                   state="risk" if streak >= 2 or daily * 100 <= -self.daily_open else self.state)

    def _available_candles(self, dataset, start, at):
        isolation = self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id")
        return self.env["golok.lab.candle"].search(Domain([
            ("dataset_id", "=", dataset.id), ("open_time", ">=", start),
            ("close_time", "<=", at), ("available_at", "<=", at), ("ingested_at", "<=", at),
        ]) & isolation, order="open_time, id", limit=400)

    def _assess_candidate(self, cycle, run, now):
        # This method is private and called only by the durable research job.
        self._lock()
        dataset = cycle.dataset_id
        session = dataset.calendar_id._sessions().get(cycle.day)
        scope = {"strategy": self.strategy, "strategy_version": strategies.VERSION, "target_policy": self.target_policy,
                 "tariff": self.tariff_id.id, "research_sha256": run.input_digest}
        at = now.replace(tzinfo=timezone.utc)
        seconds = market_data.INTERVALS[dataset.interval]
        if (self.state != "active" or not self.strategy or not self.target_policy or not session or not seconds
                or session.kind != "regular" or not session.opening < at < session.entry_cutoff
                or now < cycle.cutoff or now - cycle.cutoff > timedelta(seconds=seconds)
                or dataset.integrity_conflict or dataset.quarantined):
            return scope, None, "SUSPENDED_STALE_OR_OUTSIDE_SESSION"
        rows = self._available_candles(dataset, session.opening.replace(tzinfo=None), cycle.cutoff)
        bars = [row._to_bar() for row in rows]
        if not fixture_execution.contiguous(bars, session.opening, seconds) or rows[-1] != cycle.observation_id:
            return scope, None, "INCOMPLETE_OR_UNAVAILABLE_CANDLES"
        scope["signal_sha256"] = _input_digest(bars, dataset.calendar_id)
        scope["observation"] = rows[-1].id
        if at - bars[-1].close_time > timedelta(seconds=seconds):
            return scope, None, "STALE_OBSERVATION"
        levels = fixture_execution.proposed_levels(strategies.REGISTRY[self.strategy], bars, session, self.target_policy, at)
        if not levels:
            return scope, None, "NO_CAUSAL_SIGNAL_OR_TARGET"
        if self.order_ids.filtered(lambda row: row.state in ("pending", "open", "unresolved")):
            return scope, None, "EXPOSURE_EXISTS"
        if self.day and cycle.day < self.day:
            return scope, None, "STALE_TRADING_DAY"
        day_changed = self.day != cycle.day
        daily_open = self.available if day_changed else self.daily_open
        daily_realized = 0 if day_changed else self.daily_realized
        entries = 0 if day_changed else self.entries
        if entries >= 3 or self.loss_streak >= 2 or daily_realized * 100 <= -daily_open:
            return scope, None, "DAILY_OR_CONSECUTIVE_LOSS_LIMIT"
        entry, stop, target = levels
        tick = Decimal(dataset.mapping_id.tick) if dataset.mapping_id else Decimal(".05")
        exchange = dataset.instrument_id.exchange
        costs = self.tariff_id._schedule()
        policy = simulation.RiskPolicy(capital=Decimal(min(self.available, daily_open)) / 100)
        size = simulation.size_long(entry, stop, target, tick, bars[-1].volume, cycle.day, exchange, costs, policy)
        if not size.quantity:
            return scope, None, size.reason
        fee = paper.paise(sum(costs.fees(cycle.day, exchange, "buy", entry, size.quantity).values()))
        risk = paper.paise(size.loss)
        if risk + self.planned_risk - min(daily_realized, 0) > daily_open // 100:
            return scope, None, "DAILY_RISK_BUDGET"
        scope.update(entry=str(entry), stop=str(stop), target=str(target), quantity=size.quantity,
                     reward=str(size.reward), loss=str(size.loss), reward_to_risk=str(size.reward / size.loss),
                     estimated_entry_fee_paise=fee, execution_policy="fixture-candle-1")
        plan = {"scenario": "observations", "dataset_id": dataset.id, "state": "pending", "quantity": size.quantity,
                "risk": risk, "reserved": paper.paise(entry * size.quantity) + fee, "entry_fee": fee,
                "limit_price": str(entry), "stop_price": str(stop), "target_price": str(target),
                "expires": min(session.entry_cutoff, at + timedelta(seconds=2 * seconds)).replace(tzinfo=None)}
        settings = {"day": cycle.day, "daily_open": daily_open, "daily_realized": daily_realized, "entries": entries}
        return scope, (plan, settings), "FIXTURE_RISK_AND_COST_CHECKS_PASSED"

    def _reserve_candidate(self, candidate, plan, settings):
        order = self.env["golok.lab.fixture.order"].with_context({}).sudo().create({
            **plan, "candidate_id": candidate.id, "account_id": self.id, "company_id": self.company_id.id,
        })
        self._post("reserved", order=order, available=-order.reserved, reserved=order.reserved, risk=order.risk, **settings)

    def _settle_observations(self, watch, at):
        self._lock()
        order = self.order_ids.filtered(lambda row: row.state in ("pending", "open") and row.candidate_id.cycle_id.watch_id == watch)[:1]
        if not order:
            return
        dataset = order.dataset_id
        if dataset.quarantined or dataset.integrity_conflict or watch.dataset_id != dataset:
            if order.state == "pending":
                self._cancel(order, "DATA_INTEGRITY")
            else:
                order.sudo().write({"state": "unresolved", "exit_reason": "DATA_INTEGRITY"})
                self._post("unresolved", order=order, state="risk")
            return
        session = dataset.calendar_id._sessions()[order.candidate_id.cycle_id.day]
        now = at.replace(tzinfo=None)
        if order.state == "pending":
            self._observe_entry(order, session, now, watch.active)
        if order.state == "open":
            self._observe_exit(order, session, now)

    def _observe_entry(self, order, session, now, watch_active):
        if now > order.expires or self.state != "active" or not watch_active:
            self._cancel(order, "ENTRY_WINDOW_EXPIRED" if now > order.expires else "SCHEDULE_OR_ACCOUNT_PAUSED")
            return
        # An order is resting before a modeled open. Record the fill only once the completed bar has arrived.
        interval = market_data.INTERVALS[order.dataset_id.interval]
        opening = session.opening.replace(tzinfo=None)
        elapsed = (order.candidate_id.generated_at - opening).total_seconds()
        start = opening + timedelta(seconds=(int(elapsed // interval) + 1) * interval)
        rows = self._available_candles(order.dataset_id, start, now)
        eligible = rows.filtered(lambda row: row.open_time < order.expires and row.available_at <= order.expires
                                 and row.ingested_at <= order.expires)
        next_open = start
        examined = order.last_entry_check_id
        for row in eligible:
            if row.open_time != next_open:
                break
            next_open = row.close_time
            examined = row
            value = fixture_execution.entry_price(row._to_bar(), Decimal(order.limit_price),
                                                   Decimal(order.stop_price), order.quantity)
            if value is None:
                continue
            fee = paper.paise(sum(self.tariff_id._schedule().fees(
                self.day, order.dataset_id.instrument_id.exchange, "buy", value, order.quantity).values()))
            cost = paper.paise(value * order.quantity) + fee
            released = order.reserved - cost
            if released < 0:
                self._cancel(order)
                return
            order.sudo().write({"state": "open", "entry_observed_at": now, "entry_candle_id": row.id,
                                "entry_paise": paper.paise(value), "entry_fee": fee, "reserved": cost})
            self._post("opened", order=order, available=released, reserved=-(cost + released), cost=cost, entries=self.entries + 1)
            return
        if examined and examined != order.last_entry_check_id:
            order.sudo().write({"last_entry_check_id": examined.id})
        if now >= order.expires:
            self._cancel(order, "ENTRY_WINDOW_EXPIRED")

    def _observe_exit(self, order, session, now):
        start = order.entry_candle_id.open_time
        cutoff = session.exit_cutoff
        next_open = start
        receipt_cutoff = min(now, session.closing.replace(tzinfo=None))
        for row in self._available_candles(order.dataset_id, start, receipt_cutoff):
            bar = row._to_bar()
            if row.open_time != next_open or bar.close_time > cutoff:
                break
            next_open = row.close_time
            if row == order.entry_candle_id:
                # Stop can be touched after a modeled entry at open. Never credit an entry-bar target.
                outcome = (Decimal(order.stop_price), "ENTRY_BAR_STOP") if bar.low <= Decimal(order.stop_price) else None
            else:
                outcome = fixture_execution.exit_result(bar, Decimal(order.stop_price), Decimal(order.target_price), cutoff)
            if outcome:
                price, reason = outcome
                fee = paper.paise(sum(self.tariff_id._schedule().fees(
                    self.day, order.dataset_id.instrument_id.exchange, "sell", price, order.quantity).values()))
                if paper.paise(price * order.quantity) - fee + self.available < 0:
                    break
                self._close_position(order, paper.paise(price), fee, now, candle=row, reason=reason)
                return
        if now >= session.closing.replace(tzinfo=None):
            order.sudo().write({"state": "unresolved", "exit_reason": "MISSING_SQUARE_OFF_OBSERVATION"})
            self._post("unresolved", order=order, state="risk")


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
    candidate_id = fields.Many2one("golok.lab.research.candidate", ondelete="restrict", index=True)
    dataset_id = fields.Many2one("golok.lab.dataset", ondelete="restrict")
    expires = fields.Datetime()
    limit_price = fields.Char()
    stop_price = fields.Char()
    target_price = fields.Char()
    entry_paise = fields.Integer()
    entry_candle_id = fields.Many2one("golok.lab.candle", ondelete="restrict")
    last_entry_check_id = fields.Many2one("golok.lab.candle", ondelete="restrict")
    exit_candle_id = fields.Many2one("golok.lab.candle", ondelete="restrict")
    exit_reason = fields.Char()

    _candidate_once = models.Constraint("UNIQUE(candidate_id)", "This candidate already has a fixture order.")


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

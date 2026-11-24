from datetime import timedelta, timezone
from decimal import Decimal

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Domain

from ..services import calendar, decision, market_data, session_clock, strategies, targets


PHASES = [(value, label) for value, label in (
    ("pre_market", "Pre-market"), ("market_opening", "Market opening"), ("intraday", "Intraday"),
    ("post_market", "Post-market"), ("closed", "Closed"), ("maintenance", "Maintenance"), ("blocked", "Blocked"))]


class SessionWatch(models.Model):
    _name = "golok.lab.session.watch"
    _description = "Fixture exchange research schedule"
    _rec_name = "dataset_id"
    _check_company_auto = True

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True, readonly=True)
    dataset_id = fields.Many2one("golok.lab.dataset", required=True, check_company=True, ondelete="restrict")
    active = fields.Boolean(default=True)
    checked_at = fields.Datetime(readonly=True)
    event_ids = fields.One2many("golok.lab.session.event", "watch_id")
    cycle_minutes = fields.Integer(default=5, required=True)
    cycle_ids = fields.One2many("golok.lab.research.cycle", "watch_id")
    gap_ids = fields.One2many("golok.lab.research.gap", "watch_id")
    paper_account_id = fields.Many2one("golok.lab.fixture.account", readonly=True, ondelete="restrict",
                                       groups="golok_ai_trading_lab_pro.group_admin")

    _dataset_watch = models.Constraint("UNIQUE(dataset_id)", "A dataset may have only one session watch.")
    _cycle_interval = models.Constraint("CHECK(cycle_minutes BETWEEN 2 AND 60)", "Set a cycle interval of 2–60 minutes.")

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su and any("paper_account_id" in values for values in vals_list):
            raise AccessError(_("Bind a research schedule through the fixture account configuration."))
        return super(SessionWatch, self.with_context(default_paper_account_id=False)).create(vals_list)

    def write(self, vals):
        if not self.env.su and ("paper_account_id" in vals or (
                {"company_id", "dataset_id"} & vals.keys() and self.sudo().mapped("paper_account_id"))):
            raise AccessError(_("The bound fixture schedule and company are immutable."))
        return super().write(vals)

    @api.constrains("dataset_id")
    def _fixture_only(self):
        for watch in self:
            if watch.dataset_id.origin != "synthetic" or watch.dataset_id.calendar_id.verification != "fixture":
                raise ValidationError(_("This scheduler requires an explicit synthetic dataset and fixture calendar."))

    @api.model
    def _cron_dispatch(self):
        self.env["golok.lab.research.job"].sudo()._cron_run_durable()
        now = fields.Datetime.now().replace(tzinfo=timezone.utc)
        for watch in self.sudo().search([], order="checked_at asc nulls first, id", limit=32):
            watch.with_company(watch.company_id)._dispatch(now)

    def _dispatch(self, at):
        self.ensure_one()
        self.env.cr.execute("SELECT id FROM golok_lab_session_watch WHERE id=%s FOR UPDATE SKIP LOCKED", (self.id,))
        if not self.env.cr.fetchone():
            return self.env["golok.lab.session.event"]
        self.invalidate_recordset(["active", "dataset_id", "checked_at", "cycle_minutes"])
        operator = self._operator()
        if operator:
            account = self._fixture_account(operator)
            if account:
                self.env["golok.lab.replay.guard"]._lock(self.dataset_id.instrument_id)
                account._settle_observations(self, at)
        if not self.active:
            return self.env["golok.lab.session.event"]
        dataset = self.dataset_id
        day = at.astimezone(calendar.IST).date()
        sessions = dataset.calendar_id._sessions()
        if self.checked_at:
            self._record_missed_intervals(sessions, at)
        previous_day = self.checked_at.replace(tzinfo=timezone.utc).astimezone(calendar.IST).date() if self.checked_at else day
        # Recover only explicit completed sessions, within the last seven calendar days.
        lower_bound = max(previous_day, day - timedelta(days=7))
        for missed_day in sorted(day_ for day_ in sessions if lower_bound <= day_ < day):
            missed = sessions[missed_day]
            if missed.kind != "closed" and missed.closing < at:
                self._record_phase(missed_day, missed, "post_market", at, recovery=True)
        previous_check = self.checked_at
        self.sudo().write({"checked_at": at.replace(tzinfo=None)})
        session = sessions.get(day)
        phase = session_clock.phase(session, at)
        event = self._record_phase(day, session, phase, at)
        if phase in ("market_opening", "intraday"):
            self._schedule_cycle(day, session, phase, at, previous_check)
        return event

    def _record_missed_intervals(self, sessions, at):
        previous = self.checked_at.replace(tzinfo=timezone.utc)
        since = max(previous, at - timedelta(days=7))
        if since >= at:
            return
        interval = timedelta(minutes=self.cycle_minutes)
        gaps = []
        for day, session in sessions.items():
            for opening, closing in session.windows():
                start, end = max(opening, since), min(closing, at)
                count = max(0, (end - start) // interval - 1)
                if count:
                    gaps.append({"watch_id": self.id, "company_id": self.company_id.id, "day": day,
                                 "starts_at": start.replace(tzinfo=None), "ends_at": end.replace(tzinfo=None),
                                 "resumed_at": at.replace(tzinfo=None), "interval_minutes": self.cycle_minutes,
                                 "missed": count})
        if gaps:
            self.env["golok.lab.research.gap"].with_context({}).sudo().create(gaps)

    def _schedule_cycle(self, day, session, phase, at, previous_check):
        dataset = self.dataset_id
        if dataset.quarantined or dataset.integrity_conflict or not market_data.INTERVALS[dataset.interval]:
            return
        cycles = self.env["golok.lab.research.cycle"].sudo()
        prior = cycles.search([("watch_id", "=", self.id), ("day", "=", day)], order="id desc", limit=1)
        cutoff = at.replace(tzinfo=None)
        if prior and (prior.state in ("queued", "claimed") or cutoff < prior.cutoff + timedelta(minutes=self.cycle_minutes)):
            return
        left = next(opening for opening, closing in session.windows() if opening <= at < closing)
        gap_start = max(left.replace(tzinfo=None), previous_check) if previous_check else cutoff
        missed = max(0, int((cutoff - gap_start).total_seconds() // (self.cycle_minutes * 60)) - 1)
        candle_model = self.env["golok.lab.candle"]
        isolation = self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id")
        latest = candle_model.search(Domain([
            ("dataset_id", "=", dataset.id), ("open_time", ">=", left.replace(tzinfo=None)),
            ("close_time", "<=", cutoff), ("available_at", "<=", cutoff),
        ]) & isolation, order="available_at desc, id desc", limit=1)
        if not latest or cycles.search_count([("watch_id", "=", self.id), ("observation_id", "=", latest.id)], limit=1):
            return
        requester = self._operator()
        if not requester:
            return
        job = self.env["golok.lab.research.job"].with_user(requester).with_company(self.company_id).create({
            "dataset_id": dataset.id, "cutoff": cutoff,
        })
        cycles.with_context({}).create({
            "company_id": self.company_id.id, "watch_id": self.id, "dataset_id": dataset.id, "job_id": job.id,
            "day": day, "phase": phase, "cutoff": cutoff, "observation_id": latest.id,
            "observation_at": latest.close_time, "available_at": latest.available_at,
            "missed_intervals": missed,
        })

    def _operator(self):
        user = self.create_uid
        if user.active and self.company_id in user.company_ids and user.has_group("golok_ai_trading_lab_pro.group_admin"):
            return user
        return self.env["res.users"]

    def _fixture_account(self, operator):
        return self.env["golok.lab.fixture.account"].with_user(operator).with_company(self.company_id).search([
            ("id", "=", self.sudo().paper_account_id.id), ("company_id", "=", self.company_id.id),
        ], limit=1)

    def _record_phase(self, day, session, phase, at, *, recovery=False):
        dataset = self.dataset_id
        events = self.env["golok.lab.session.event"].sudo()
        domain = [("watch_id", "=", self.id), ("day", "=", day), ("phase", "=", phase)]
        known = events.search(domain, limit=1)
        if known:
            return known
        vals = {"watch_id": self.id, "company_id": self.company_id.id, "day": day, "phase": phase,
                "observed_at": at.replace(tzinfo=None), "mode": "fixture", "state": "completed",
                "summary": "NO TRADE · fixture research only", "recovered": recovery}
        if phase in ("market_opening", "intraday", "post_market"):
            cutoff = min(at, session.closing).replace(tzinfo=None)
            eligible = self.env["golok.lab.candle"].search_count(Domain([
                ("dataset_id", "=", dataset.id), ("available_at", "<=", cutoff),
                ("close_time", ">=", session.opening.replace(tzinfo=None))])
                & self.env["golok.lab.holdout"]._observation_domain("close_time", "close_time", "instrument_id"))
            vals["observation_count"] = eligible
            if eligible and not dataset.quarantined:
                try:
                    with self.env.cr.savepoint():
                        result = self.env["golok.lab.run"].create({"dataset_id": dataset.id, "as_of": cutoff})
                    vals["run_id"] = result.id
                except (AccessError, UserError):
                    vals.update(state="blocked", summary="NO TRADE · fixture research unavailable")
            else:
                vals.update(state="blocked", summary="NO TRADE · no permitted observations by cutoff")
        elif phase == "blocked" or dataset.quarantined:
            vals.update(state="blocked", summary="NO TRADE · calendar or data unavailable")
        if phase == "post_market":
            previous = events.search_count([("watch_id", "=", self.id), ("day", "=", day),
                                            ("phase", "in", ("pre_market", "market_opening", "intraday"))])
            vals["summary"] += f" · {previous} recorded earlier phases"
        if recovery:
            vals["summary"] += " · historical recovery"
        return events.create(vals)

    def action_check_now(self):
        self.ensure_one()
        self.check_access("read")
        if self.company_id != self.env.company or not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise AccessError(_("A schedule administrator in the active company is required."))
        record = self._dispatch(fields.Datetime.now().replace(tzinfo=timezone.utc))
        if not record:
            return False
        return {"type": "ir.actions.act_window", "res_model": record._name, "res_id": record.id,
                "views": [(False, "form")]}


class SessionEvent(models.Model):
    _name = "golok.lab.session.event"
    _description = "Exchange research phase report"
    _rec_name = "summary"
    _order = "day desc, observed_at desc, id desc"

    watch_id = fields.Many2one("golok.lab.session.watch", required=True, ondelete="restrict")
    company_id = fields.Many2one("res.company", required=True, index=True)
    day = fields.Date(required=True, index=True)
    phase = fields.Selection(PHASES, required=True)
    observed_at = fields.Datetime(required=True)
    mode = fields.Selection([("fixture", "Fixture-only research")], required=True)
    state = fields.Selection([("completed", "Completed"), ("blocked", "Blocked")], required=True)
    summary = fields.Char(required=True)
    observation_count = fields.Integer()
    recovered = fields.Boolean(readonly=True)
    run_id = fields.Many2one("golok.lab.run", ondelete="restrict")

    _phase_once = models.Constraint("UNIQUE(watch_id,day,phase)", "This phase has already been recorded.")


class ResearchCycle(models.Model):
    _name = "golok.lab.research.cycle"
    _description = "Recurring fixture research cycle"
    _order = "id desc"
    _rec_name = "observation_at"

    company_id = fields.Many2one("res.company", required=True, index=True)
    watch_id = fields.Many2one("golok.lab.session.watch", required=True, index=True, ondelete="restrict")
    dataset_id = fields.Many2one("golok.lab.dataset", required=True, ondelete="restrict")
    job_id = fields.Many2one("golok.lab.research.job", required=True, ondelete="restrict", index=True)
    day = fields.Date(required=True, index=True)
    phase = fields.Selection(PHASES, required=True)
    cutoff = fields.Datetime(required=True)
    observation_id = fields.Many2one("golok.lab.candle", required=True, ondelete="restrict",
                                      groups="golok_ai_trading_lab_pro.group_admin")
    observation_at = fields.Datetime(required=True)
    available_at = fields.Datetime(required=True)
    missed_intervals = fields.Integer(readonly=True)
    state = fields.Selection(related="job_id.state")
    run_id = fields.Many2one(related="job_id.run_id")
    processed_at = fields.Datetime(related="job_id.finished_at")
    elapsed_ms = fields.Float(related="job_id.elapsed_ms")
    failure_reason = fields.Char(related="job_id.failure_reason")
    candidate_ids = fields.One2many("golok.lab.research.candidate", "cycle_id")

    _observation_once = models.Constraint("UNIQUE(watch_id,observation_id)", "This observation was already scheduled.")
    _job_once = models.Constraint("UNIQUE(job_id)", "A job already belongs to a research cycle.")

    def _validate_execution(self, requester):
        self.ensure_one()
        if (not self.watch_id.active or self.watch_id.dataset_id != self.dataset_id
                or self.company_id not in requester.company_ids
                or not requester.has_group("golok_ai_trading_lab_pro.group_admin")):
            raise AccessError(_("The schedule was paused or changed."))
        available = self.env["golok.lab.candle"].with_user(requester).search_count(
            [("id", "=", self.observation_id.id)], limit=1)
        if not available:
            raise AccessError(_("The scheduled observation is no longer eligible."))

    def _lock_competition(self):
        self.ensure_one()
        account = self.watch_id.sudo().paper_account_id
        if account:
            self.env["golok.lab.replay.guard"]._lock(account.bound_watch_ids.dataset_id.instrument_id)

    def _publish_completed(self):
        """Publish an account's exact-cutoff cohort in one transaction."""
        self.ensure_one()
        account = self.watch_id.sudo().paper_account_id
        now = fields.Datetime.now()
        if not account:
            if self.run_id and not self.candidate_ids:
                self._save_candidate(self.run_id, account, now, {}, None, {},
                                     "Descriptive fixture research has no bound paper account.")
            return
        cohort = self.search([("company_id", "=", self.company_id.id), ("day", "=", self.day),
                              ("watch_id", "in", account.bound_watch_ids.ids), ("cutoff", "=", self.cutoff)])
        if any(job.state in ("queued", "claimed") for job in cohort.job_id):
            return
        closed_cohort = bool(cohort.candidate_ids)
        profiles = []
        for cycle in cohort.sorted(lambda row: (row.dataset_id.instrument_id.symbol, row.dataset_id.id)):
            job = cycle.job_id
            if not job.run_id or cycle.candidate_ids:
                continue
            requester = job.requested_by
            scoped = cycle.with_company(cycle.company_id)
            run = job.run_id.with_user(requester).with_company(cycle.company_id)
            operator_account = scoped.watch_id._fixture_account(requester)
            if not operator_account or not requester.active:
                continue
            try:
                scoped._validate_execution(requester)
            except AccessError:
                continue
            operator_account._lock()
            scope, reservation, reason = operator_account._assess_candidate(scoped, run, now)
            checks = scoped._candidate_checks(run, operator_account, scope, reservation, now)
            rank = (targets.rank_values(Decimal(scope["reward"]), Decimal(scope["loss"]), scope["volume"])
                    if reservation and all(checks.values()) else None)
            profiles.append((scoped, run, operator_account, scope, reservation, checks, reason, rank))
        winner = max((item for item in profiles if item[-1] is not None), key=lambda item: item[-1], default=None)
        for profile in profiles:
            cycle, run, operator_account, scope, reservation, checks, reason, rank = profile
            scope["competition"] = {"cutoff": fields.Datetime.to_string(self.cutoff), "cycle_ids": sorted(cohort.ids),
                                    "winning_cycle_id": winner[0].id if winner and not closed_cohort else None}
            if rank is not None and (profile is not winner or closed_cohort):
                checks["G11"] = ("Other or finalized candidate", "One account reservation per cutoff", False)
                reason = "COHORT_ALREADY_FINALIZED" if closed_cohort else "OUTRANKED_IN_COHORT"
            cycle._save_candidate(run, operator_account, now, scope, reservation, checks, reason)

    def _candidate_checks(self, run, account, scope, reserved, generated):
        self.ensure_one()
        checks = {
            "G01": run.dataset_id.origin == "synthetic",
            "G02": bool(run.dataset_id.instrument_id),
            "G03": run.dataset_id.calendar_id.verification == "fixture",
            "G04": bool(run.bar_count and not run.gap_count),
            "G05": self.available_at <= self.cutoff,
        }
        if reserved:
            plan, settings = reserved
            checks.update({
                "G06": Decimal(plan["stop_price"]) < Decimal(plan["limit_price"]) < Decimal(plan["target_price"]),
                "G07": scope["strategy"] in strategies.REGISTRY,
                "G08": account.mode == "fixture" and run.dataset_id.origin == "synthetic",
                "G09": scope["tariff"] == account.tariff_id.id and plan["entry_fee"] >= 0,
                "G10": plan["quantity"] > 0 and Decimal(scope["reward_to_risk"]) >= 2,
                "G11": plan["reserved"] <= account.available and account.planned_risk == 0 and settings["entries"] < 3,
                "G12": generated < plan["expires"],
                "G13": scope["observation"] == self.observation_id.id and len(scope["signal_sha256"]) == 64,
                "G14": self.watch_id in account.bound_watch_ids and account.company_id == self.company_id,
            })
        return checks

    def _save_candidate(self, run, account, generated, scope, reserved, checks, reason):
        if not checks:
            checks = self._candidate_checks(run, account, scope, reserved, generated)
        permitted = bool(reserved) and all(value is True for value in checks.values())
        evaluation = decision.evaluate(checks, mode="synthetic_replay" if permitted else "fixture_research",
                                       context={"dataset_version": scope.get("signal_sha256", run.input_digest),
                                                "execution_scope": "PROSPECTIVE_FIXTURE" if account else "DESCRIPTIVE_FIXTURE"})
        state = "paper_eligible" if permitted else "no_trade"
        if not account:
            state = "experimental"
        elif not permitted:
            if reason in ("NO_CAUSAL_SIGNAL_OR_TARGET", "INCOMPLETE_OR_UNAVAILABLE_CANDLES"):
                state = "watch"
            elif reason in ("STALE_OBSERVATION", "STALE_TRADING_DAY"):
                state = "expired"
            elif reason != "SUSPENDED_STALE_OR_OUTSIDE_SESSION":
                state = "rejected"
        candidate = self.env["golok.lab.research.candidate"].with_context({}).sudo().create({
            "cycle_id": self.id, "company_id": self.company_id.id, "input_digest": run.input_digest,
            "engine_version": run.engine_version,
            "evidence": {"research": run.evidence, "decision": evaluation, "fixture_plan": scope},
            "reason": reason, "generated_at": generated,
            "state": state,
        })
        if permitted:
            account._reserve_candidate(candidate, *reserved)


class ResearchCandidate(models.Model):
    _name = "golok.lab.research.candidate"
    _description = "Immutable fixture research outcome"
    _rec_name = "reason"
    _order = "id desc"

    cycle_id = fields.Many2one("golok.lab.research.cycle", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    input_digest = fields.Char(required=True)
    engine_version = fields.Char(required=True)
    evidence = fields.Json(required=True)
    reason = fields.Char(required=True)
    state = fields.Selection([("no_trade", "NO TRADE"), ("experimental", "Experimental"),
                              ("watch", "Watch"), ("rejected", "Rejected"), ("expired", "Expired"),
                              ("paper_eligible", "Fixture paper eligible")], required=True, default="no_trade")
    generated_at = fields.Datetime()
    order_ids = fields.One2many("golok.lab.fixture.order", "candidate_id")
    lifecycle = fields.Selection([("no_trade", "NO TRADE"), ("experimental", "Experimental"),
                                  ("watch", "Watch"), ("rejected", "Rejected"), ("expired", "Expired"),
                                  ("invalidated", "Invalidated"), ("wait", "Waiting for entry"),
                                  ("paper_eligible", "Fixture paper eligible"),
                                  ("pending", "Paper pending"), ("open", "Paper open"), ("closed", "Paper closed"),
                                  ("cancelled", "Paper cancelled"), ("unresolved", "Reconciliation required")],
                                 compute="_compute_lifecycle")

    @api.depends("state", "order_ids.state", "order_ids.exit_reason", "order_ids.last_entry_check_id")
    def _compute_lifecycle(self):
        for item in self:
            order = item.order_ids[:1]
            if order.state == "cancelled" and order.exit_reason in ("DATA_INTEGRITY", "ENTRY_WINDOW_EXPIRED"):
                item.lifecycle = "invalidated" if order.exit_reason == "DATA_INTEGRITY" else "expired"
            elif order.state == "pending" and order.last_entry_check_id:
                item.lifecycle = "wait"
            else:
                item.lifecycle = order.state or item.state

    _cycle_once = models.Constraint("UNIQUE(cycle_id)", "Research outcome already published.")


class ResearchGap(models.Model):
    _name = "golok.lab.research.gap"
    _description = "Elapsed fixture research operating interval"
    _order = "starts_at desc, id desc"

    watch_id = fields.Many2one("golok.lab.session.watch", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    day = fields.Date(required=True)
    starts_at = fields.Datetime(required=True)
    ends_at = fields.Datetime(required=True)
    resumed_at = fields.Datetime(required=True)
    interval_minutes = fields.Integer(required=True)
    missed = fields.Integer(required=True)

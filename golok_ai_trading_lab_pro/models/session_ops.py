from datetime import timedelta, timezone

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Domain

from ..services import calendar, decision, market_data, session_clock


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

    _dataset_watch = models.Constraint("UNIQUE(dataset_id)", "A dataset may have only one session watch.")
    _cycle_interval = models.Constraint("CHECK(cycle_minutes BETWEEN 2 AND 60)", "Set a cycle interval of 2–60 minutes.")

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
        if not self.active:
            return self.env["golok.lab.session.event"]
        dataset = self.dataset_id
        day = at.astimezone(calendar.IST).date()
        sessions = dataset.calendar_id._sessions()
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
        requester = self.create_uid
        if (not requester.active or self.company_id not in requester.company_ids
                or not requester.has_group("golok_ai_trading_lab_pro.group_admin")):
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

    def _publish(self, run):
        self.ensure_one()
        if self.candidate_ids:
            if self.candidate_ids.input_digest != run.input_digest:
                raise ValidationError(_("A different input cannot replace a published research outcome."))
            return
        checks = {
            "G01": run.dataset_id.origin == "synthetic",
            "G02": bool(run.dataset_id.instrument_id),
            "G03": run.dataset_id.calendar_id.verification == "fixture",
            "G04": bool(run.bar_count and not run.gap_count),
            "G05": self.available_at <= self.cutoff,
        }
        evaluation = decision.evaluate(checks, mode="fixture_research", context={"dataset_version": run.input_digest})
        self.env["golok.lab.research.candidate"].with_context({}).sudo().create({
            "cycle_id": self.id, "company_id": self.company_id.id, "input_digest": run.input_digest,
            "engine_version": run.engine_version, "evidence": {"research": run.evidence, "decision": evaluation},
            "reason": "Descriptive fixture research has no validated entry, tariff and risk approval.",
        })


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
    state = fields.Selection([("no_trade", "NO TRADE")], required=True, default="no_trade")

    _cycle_once = models.Constraint("UNIQUE(cycle_id)", "Research outcome already published.")

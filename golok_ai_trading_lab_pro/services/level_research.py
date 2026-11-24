"""Causal long-side entry, stop and target research with explicit vetoes."""

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

from . import indicators, simulation, targets

VERSION = "entry-stop-target-1"
MAX_HISTORY = 40


def _tick(price, tick, rounding):
    return (price / tick).to_integral_value(rounding=rounding) * tick


def completed(history, as_of):
    return [bar for bar in history if bar.available_at is not None and bar.close_time <= bar.available_at < as_of]


def evaluate(history, session, as_of, expiry, baseline_stop, tick, exchange, costs, risk):
    """Return auditable experimental levels using only information available before as_of."""
    bars = completed(history, as_of)[-MAX_HISTORY:]
    if not bars or not as_of < min(expiry, session.entry_cutoff, session.exit_cutoff) or tick <= 0:
        return {"version": VERSION, "status": "NO_TRADE", "reason": "MISSING_HISTORY_OR_EXPIRED"}
    signal = bars[-1]
    atr = indicators.calculate(bars)["atr14"][-1]
    if not atr or signal.volume <= 0:
        return {"version": VERSION, "status": "NO_TRADE", "reason": "VOLATILITY_OR_LIQUIDITY_UNAVAILABLE"}
    prior = bars[-11:-1]
    ceiling = _tick(min(signal.close * Decimal("1.01"), signal.close + atr / 2), tick, ROUND_FLOOR)
    support = max((bar.low for bar in prior if bar.low < signal.close), default=signal.close - atr)
    floor = _tick(max(support, signal.close - atr), tick, ROUND_CEILING)
    volume = sum(bar.volume for bar in bars)
    vwap = sum((bar.high + bar.low + bar.close) * bar.volume for bar in bars) / (3 * volume)
    breakout = max(bar.high for bar in prior)
    entries = {"signal": signal.close, "pullback_vwap": vwap, "prior_breakout": breakout}
    alternatives = []
    for entry_kind, raw_entry in entries.items():
        entry = _tick(raw_entry, tick, ROUND_FLOOR)
        if not floor <= entry <= ceiling:
            continue
        stops = {"strategy": baseline_stop, "swing": min(bar.low for bar in bars[-3:]),
                 "atr": entry - atr, "volatility_buffer": support - atr / 2}
        for stop_kind, raw_stop in stops.items():
            stop = _tick(raw_stop, tick, ROUND_FLOOR)
            if not 0 < stop < entry:
                continue
            levels, reason = targets.levels(bars, entry, stop, "atr_barrier", as_of, session.exit_cutoff)
            if not levels:
                continue
            target = _tick(levels[0], tick, ROUND_FLOOR)
            sizing = simulation.size_long(entry, stop, target, tick, signal.volume, session.day, exchange, costs, risk)
            alternatives.append({"entry_method": entry_kind, "stop_method": stop_kind, "limit": entry,
                                 "stop": stop, "target": target, "target_reason": reason,
                                 "risk_distance": entry - stop, "atr": atr, "liquidity": signal.volume,
                                 "quantity": sizing.quantity, "net_reward": sizing.reward, "modeled_loss": sizing.loss,
                                 "sizing_reason": sizing.reason,
                                 "priority": targets.rank(sizing, signal.volume)})
    eligible = [row for row in alternatives if row["quantity"] > 0]
    return {"version": VERSION, "status": "RESEARCH_PROPOSAL" if eligible else "NO_TRADE",
            "reason": "CAUSAL_NET_FEASIBILITY" if eligible else "NO_FEASIBLE_LEVELS",
            "reference": signal.close, "range": (floor, ceiling), "evaluated_at": as_of,
            "expires": min(expiry, session.entry_cutoff),
            "selected": max(eligible, key=lambda row: row["priority"], default=None), "alternatives": alternatives}


def eligible_open(proposal, opens_at, opening):
    """Check a subsequent simulated opening without changing the proposal."""
    return (proposal["status"] == "RESEARCH_PROPOSAL" and proposal["evaluated_at"] < opens_at < proposal["expires"]
            and proposal["range"][0] <= opening <= proposal["selected"]["limit"])

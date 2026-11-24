"""ST-01 research-only replay of a complete, explicitly synthetic equity session."""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import timedelta
from decimal import Decimal, localcontext
from pathlib import Path

from .calendar import validate_bar
from .simulation import FRICTION, RiskPolicy, size_long

VERSION = "ST-01/1"


@dataclass(frozen=True)
class OpeningRangeVersion:
    opening_minutes: int = 15
    volume_multiple: Decimal = Decimal("1.5")
    max_entry_deviation: Decimal = Decimal("0.01")
    max_range_fraction: Decimal = Decimal("0.04")
    target_multiple: int = 4
    max_hold_bars: int = 12


def canonical(value):
    return json.dumps(value, default=str, sort_keys=True, separators=(",", ":"))


def _exit_trade(bars, from_index, stop, target, cutoff, max_bars):
    for count, bar in enumerate(bars[from_index:], 1):
        if bar.open <= stop:
            return bar.open, bar.open_time, "GAP_OR_OPEN_STOP"
        if bar.low <= stop:
            return stop, bar.close_time, "STOP_AMBIGUITY" if bar.high > target else "STOP"
        if bar.open > target or bar.high > target:
            return target, bar.close_time, "CONSERVATIVE_TARGET"
        if bar.close_time >= cutoff or count >= max_bars:
            return bar.close, bar.close_time, "SESSION_EXIT" if bar.close_time >= cutoff else "TIME_EXIT"
    raise ValueError("No bounded closing observation.")


def replay(bars, session, exchange, seconds, tick, costs, *, source, partition, origin, risk=RiskPolicy()):
    """Freeze inputs and replay a fully sampled synthetic regular session."""
    if origin != "synthetic" or not source or partition not in ("train", "validation", "holdout"):
        raise ValueError("This replay only accepts explicitly labeled synthetic experiments and a declared partition.")
    if (session.kind != "regular" or type(seconds) is not int or seconds not in (60, 180, 300, 900)
            or not isinstance(tick, Decimal) or not tick.is_finite() or tick <= 0 or exchange not in ("NSE", "BSE")):
        raise ValueError("ST-01 requires a regular equity session, supported interval and positive tick.")
    params = OpeningRangeVersion()
    bars = tuple(bars)
    slots = session.slots(seconds)
    if [(bar.open_time, bar.close_time) for bar in bars] != slots:
        raise ValueError("The session requires a complete ordered grid.")
    for bar in bars:
        validate_bar(bar, {session.day: session}, seconds)
        if bar.available_at < bar.close_time or any(price % tick for price in (bar.open, bar.high, bar.low, bar.close)):
            raise ValueError("Candles must be available after close and conform to the tick size.")
    if session.exit_cutoff not in {close for _, close in slots}:
        raise ValueError("The exit cutoff must match a candle close.")
    window_end = session.opening + timedelta(minutes=params.opening_minutes)
    opening = [bar for bar in bars if bar.close_time <= window_end]
    if not opening or opening[-1].close_time != window_end:
        raise ValueError("The opening range is incomplete.")
    upper, lower = max(bar.high for bar in opening), min(bar.low for bar in opening)

    specification = {
        "version": VERSION, "params": asdict(params), "risk": asdict(risk),
        "costs": [asdict(tariff) for tariff in costs.tariffs], "source": source, "origin": origin,
        "partition": partition, "exchange": exchange, "tick": tick, "interval_seconds": seconds,
        "session": asdict(session),
        "bars_digest": hashlib.sha256(canonical([asdict(bar) for bar in bars]).encode()).hexdigest(),
        "implementation_digests": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ("backtest.py", "calendar.py", "simulation.py")
        },
    }
    experiment = hashlib.sha256(canonical(specification).encode()).hexdigest()
    candidates = []
    trade = None
    with localcontext() as ctx:
        ctx.prec = 28
        for index in range(len(opening), len(bars)):
            bar = bars[index]
            if bar.high <= upper or bars[index - 1].close > upper:
                continue
            event = {"decision_time": bar.available_at, "observation": bar.close_time}
            candidates.append(event)
            previous = bars[max(0, index - 3):index]
            average_volume = Decimal(sum(row.volume for row in previous)) / len(previous)
            if trade is not None:
                event["reason"] = "DAILY_ENTRY_LIMIT"
            elif bar.available_at >= session.entry_cutoff:
                event["reason"] = "ENTRY_CUTOFF"
            elif any(row.available_at > bar.available_at for row in (*opening, *previous)):
                event["reason"] = "POINT_IN_TIME_INPUT_MISSING"
            elif bar.close <= upper:
                event["reason"] = "FALSE_BREAKOUT"
            elif not average_volume or bar.volume < params.volume_multiple * average_volume:
                event["reason"] = "LOW_VOLUME"
            elif upper - lower > upper * params.max_range_fraction:
                event["reason"] = "OPENING_RANGE_TOO_WIDE"
            else:
                # An open at the same instant as publication is unavailable to this decision.
                fill_index = next((j for j in range(index + 1, len(bars)) if bars[j].open_time > bar.available_at), None)
                if fill_index is None:
                    event["reason"] = "EXPIRED"
                    continue
                fill = bars[fill_index]
                if (fill.open_time >= session.entry_cutoff or fill.open_time >= session.exit_cutoff
                        or fill.open_time > bar.available_at + timedelta(seconds=seconds)):
                    event["reason"] = "EXPIRED"
                    continue
                if fill.open <= upper or fill.open > bar.close * (1 + params.max_entry_deviation):
                    event["reason"] = "ENTRY_DEVIATION"
                    continue
                target = fill.open + (fill.open - lower) * params.target_multiple
                sizing = size_long(fill.open, lower, target, tick, bar.volume, session.day, exchange, costs, risk)
                event["reason"] = sizing.reason
                if not sizing.quantity:
                    continue
                price, moment, why = _exit_trade(bars, fill_index, lower, target, session.exit_cutoff, params.max_hold_bars)
                buy = costs.fees(session.day, exchange, "buy", fill.open, sizing.quantity)
                sell = costs.fees(session.day, exchange, "sell", price, sizing.quantity)
                total_fees = sum(buy.values()) + sum(sell.values())
                gross = (price - fill.open) * sizing.quantity
                trade = {"quantity": sizing.quantity, "entry": fill.open, "entry_time": fill.open_time,
                         "stop": lower, "target": target, "exit": price, "exit_time": moment, "exit_reason": why,
                         "gross": gross, "costs": total_fees, "net": gross - total_fees, "buy_fees": buy, "sell_fees": sell,
                         "friction": sum(buy[k] + sell[k] for k in FRICTION)}
    net = trade["net"] if trade else None
    gross = trade["gross"] if trade else None
    return {
        "experiment": experiment, "specification": specification, "status": "SYNTHETIC_CORRECTNESS_ONLY",
        "candidates": candidates, "trade": trade,
        "metrics": {"trade_count": int(trade is not None), "net": net,
                    "drawdown_closed_equity": max(-net, 0) if net is not None else None,
                    "equity_closed": [risk.capital, risk.capital + net] if net is not None else [risk.capital],
                    "gross_profit": max(gross, 0) if gross is not None else None,
                    "gross_loss": max(-gross, 0) if gross is not None else None,
                    "costs": trade["costs"] if trade else None,
                    "outcome": ("WIN" if net > 0 else "LOSS" if net < 0 else "NEUTRAL") if net is not None else None},
    }

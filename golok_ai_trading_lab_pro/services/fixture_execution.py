"""Causal rules for paper execution on an explicitly synthetic candle stream."""

from datetime import timedelta

from . import targets


def contiguous(bars, opening, seconds):
    for bar in bars:
        if bar.open_time != opening or bar.close_time != opening + timedelta(seconds=seconds):
            return False
        opening = bar.close_time
    return bool(bars)


def observation_freshness(observed, available, received, cutoff, evaluated, seconds):
    if not seconds or not all((observed, available, received, cutoff, evaluated)):
        return "UNKNOWN"
    if not observed <= available <= cutoff <= evaluated or not observed <= received <= cutoff:
        return "NOT_AVAILABLE_AT_CUTOFF"
    return "STALE" if evaluated - observed > timedelta(seconds=seconds) else "WITHIN_INTERVAL"


def proposed_levels(strategy, bars, session, policy, observed_at):
    stop = strategy.signal(bars, session)
    entry = bars[-1].close
    if stop is None:
        return None
    found, _reason = targets.levels(bars, entry, stop, policy, observed_at, session.exit_cutoff)
    return (entry, stop, found[0]) if found else None


def entry_price(bar, limit, stop, quantity):
    if bar.volume >= 100 * quantity and stop < bar.open <= limit:
        return bar.open
    return None


def exit_result(bar, stop, target, cutoff):
    if bar.open <= stop:
        return bar.open, "GAP_STOP"
    if bar.low <= stop:
        return stop, "STOP_FIRST" if bar.high >= target else "STOP"
    if bar.high >= target:
        return target, "TARGET"
    if bar.close_time == cutoff:
        return bar.close, "SQUARE_OFF"
    return None

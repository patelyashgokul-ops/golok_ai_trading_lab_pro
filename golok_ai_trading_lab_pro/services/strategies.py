"""Causal experimental signal definitions for the portfolio replay."""

from dataclasses import dataclass
from decimal import Decimal

VERSION = "portfolio-1"


@dataclass(frozen=True)
class Strategy:
    code: str
    name: str
    hypothesis: str
    signal: object


def opening_breakout(bars, session):
    from datetime import timedelta

    end = session.opening + timedelta(minutes=15)
    opening = [item for item in bars if item.close_time <= end]
    if not opening or opening[-1].close_time != end or bars[-1].close_time <= end or len(bars) < 4:
        return None
    upper, lower = max(b.high for b in opening), min(b.low for b in opening)
    previous = bars[-4:-1]
    if (bars[-2].close <= upper < bars[-1].close and upper - lower <= upper * Decimal(".04")
            and sum(b.volume for b in previous) > 0
            and bars[-1].volume * 2 >= sum(b.volume for b in previous)):
        return lower
    return None


def vwap_reclaim_pullback(bars, session):
    if len(bars) < 6:
        return None
    earlier = bars[:-1]
    volume = sum(bar.volume for bar in earlier)
    if not volume:
        return None
    anchor = sum((bar.high + bar.low + bar.close) * bar.volume for bar in earlier) / (3 * volume)
    current, previous = bars[-1], bars[-2]
    if (previous.close > earlier[0].close and previous.close > anchor
            and current.low <= anchor < current.close and current.close > current.open):
        return min(current.low, previous.low)
    return None


def range_reversion(bars, session):
    if len(bars) < 7:
        return None
    reference, current = bars[-7:-1], bars[-1]
    high, low = max(b.high for b in reference), min(b.low for b in reference)
    width = high - low
    if (width > 0 and abs(reference[-1].close - reference[0].close) <= width / 4
            and current.low < low < current.close <= low + width / 2 and current.close > current.open):
        return current.low
    return None


REGISTRY = {
    row.code: row for row in (
        Strategy("ST-01", "Opening Range Breakout", "Volume confirmed close above the completed opening range.", opening_breakout),
        Strategy("ST-02", "VWAP Pullback", "Continuation after a rising session pulls back to prior approximated VWAP.", vwap_reclaim_pullback),
        Strategy("ST-08", "Mean Reversion", "A range-bound series rejects a downside excursion and closes back inside.", range_reversion),
    )
}

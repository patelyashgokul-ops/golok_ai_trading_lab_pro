"""Independent causal definitions for additional historical research findings."""

from collections import Counter
from dataclasses import dataclass

VERSION = "1"


@dataclass(frozen=True)
class Engine:
    name: str
    minimum: int
    evaluate: object


def price_structure(bars):
    window = bars[-6:]
    pairs = list(zip(window, window[1:]))
    return {
        "higher_highs": sum(right.high > left.high for left, right in pairs),
        "lower_lows": sum(right.low < left.low for left, right in pairs),
        "net_close_change": str(window[-1].close - window[0].close),
    }


def candle_shape(bars):
    bar = bars[-1]
    spread = bar.high - bar.low
    body = abs(bar.close - bar.open)
    upper = bar.high - max(bar.close, bar.open)
    lower = min(bar.close, bar.open) - bar.low
    shape = ("flat" if not spread else "doji" if body * 10 <= spread else
             "lower_rejection" if lower >= 2 * body and upper <= body else
             "upper_rejection" if upper >= 2 * body and lower <= body else "unclassified")
    return {"shape": shape, "body": str(body), "upper_wick": str(upper), "lower_wick": str(lower)}


def levels(bars):
    previous = bars[-21:-1]
    return {"rolling_support": str(min(bar.low for bar in previous)),
            "rolling_resistance": str(max(bar.high for bar in previous)), "preceding_observations": 20}


def momentum(bars):
    recent = bars[-11:]
    moves = [right.close - left.close for left, right in zip(recent, recent[1:])]
    signs = Counter((move > 0) - (move < 0) for move in moves)
    return {"up_closes": signs[1], "down_closes": signs[-1], "flat_closes": signs[0],
            "net_return": str(recent[-1].close / recent[0].close - 1)}


REGISTRY = {
    "RE-03": Engine("Price structure", 6, price_structure),
    "RE-04": Engine("Candle shape", 1, candle_shape),
    "RE-06": Engine("Preceding support and resistance", 21, levels),
    "RE-19": Engine("Directional momentum", 11, momentum),
}


def analyze(bars, quality_warning=False):
    if len(bars) > 250:
        raise ValueError("Use a verified snapshot of at most 250 bars.")
    results = {}
    for key, engine in REGISTRY.items():
        eligible = len(bars) >= engine.minimum and not quality_warning
        results[key] = {
            "engine": key, "version": VERSION, "name": engine.name, "minimum": engine.minimum,
            "status": "COMPLETED" if eligible else "INSUFFICIENT_DATA",
            "observations": len(bars), "required": ["Ordered OHLCV"],
            "warning": "Snapshot has missing or unverifiable observations." if quality_warning else None,
            "finding": engine.evaluate(bars) if eligible else None,
        }
    return results

"""Independent causal definitions for additional historical research findings."""

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from statistics import median

VERSION = "3"


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


def breakout(bars):
    current = bars[-1]
    prior_high = max(bar.high for bar in bars[-11:-1])
    prior_low = min(bar.low for bar in bars[-11:-1])
    direction = "up" if current.close > prior_high else "down" if current.close < prior_low else "inside"
    return {"direction": direction, "prior_high": str(prior_high), "prior_low": str(prior_low)}


def failed_breakout(bars):
    prior_high = max(bar.high for bar in bars[-12:-2])
    prior_low = min(bar.low for bar in bars[-12:-2])
    excursion, current = bars[-2:]
    return {"failed_up": excursion.close > prior_high >= current.close >= prior_low,
            "failed_down": excursion.close < prior_low <= current.close <= prior_high,
            "prior_high": str(prior_high), "prior_low": str(prior_low)}


def instrument_regime(bars):
    closes = [bar.close for bar in bars[-21:]]
    steps = [right / left - 1 for left, right in zip(closes, closes[1:])]
    direction = closes[-1] / closes[0] - 1
    travel = sum(abs(step) for step in steps)
    strength = abs(direction) / travel if travel else 0
    movement = median(abs(step) for step in steps)
    return {"trend": "up" if strength >= Decimal(".5") and direction > 0 else
            "down" if strength >= Decimal(".5") and direction < 0 else "range",
            "directional_return": str(direction),
            "momentum": "up" if sum(steps[-5:]) > 0 else "down" if sum(steps[-5:]) < 0 else "flat",
            "efficiency": str(strength), "median_absolute_return": str(movement),
            "volatility": "high" if movement >= Decimal(".02") else "low",
            "stress": abs(steps[-1]) > max(movement * 4, Decimal(".02")), "scope": "instrument_only"}


def turnover_proxy(bars):
    recent = bars[-20:]
    return {"median_close_times_volume": str(median(bar.close * bar.volume for bar in recent)),
            "zero_volume_observations": sum(bar.volume == 0 for bar in recent)}


def abnormal_activity(bars):
    baseline = bars[-21:-1]
    center = median(bar.volume for bar in baseline)
    width = median((bar.high - bar.low) / bar.close for bar in baseline)
    current = bars[-1]
    spread = (current.high - current.low) / current.close
    return {"volume_ratio": str(Decimal(current.volume) / Decimal(center)) if center else None,
            "range_ratio": str(spread / width) if width else None,
            "volume_expansion": current.volume > 3 * center if center else None,
            "range_expansion": spread > 3 * width if width else None}


REGISTRY = {
    "RE-03": Engine("Price structure", 6, price_structure),
    "RE-04": Engine("Candle shape", 1, candle_shape),
    "RE-06": Engine("Preceding support and resistance", 21, levels),
    "RE-07": Engine("Close outside a preceding ten-bar range", 11, breakout),
    "RE-08": Engine("Close back inside the pre-breakout range", 12, failed_breakout),
    "RE-09": Engine("Instrument regime", 21, instrument_regime),
    "RE-17": Engine("Median turnover proxy", 20, turnover_proxy),
    "RE-20": Engine("Volume and range anomalies versus a prior twenty-bar baseline", 21, abnormal_activity),
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

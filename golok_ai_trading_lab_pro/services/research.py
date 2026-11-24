"""Deterministic descriptive research over already-closed candles."""

from decimal import Decimal, localcontext

VERSION = "1"
ENGINES = {"RE-01": "Technical Analysis", "RE-05": "Volume Intelligence", "RE-18": "Volatility Analysis"}


def mean(values):
    return sum(values, Decimal(0)) / len(values)


def describe(bars):
    """Use only the supplied observations and a fixed decimal context."""
    with localcontext() as context:
        context.prec = 28
        closes = [bar.close for bar in bars]
        sma = mean(closes[-20:]) if len(closes) >= 20 else None
        relative_volume = None
        if len(bars) >= 21:
            baseline = mean([bar.volume for bar in bars[-21:-1]])
            if baseline:
                relative_volume = Decimal(bars[-1].volume) / baseline
        atr = None
        if len(bars) >= 15:
            ranges = [
                max(bar.high - bar.low, abs(bar.high - previous.close), abs(bar.low - previous.close))
                for previous, bar in zip(bars, bars[1:])
            ]
            atr = mean(ranges[:14])
            for true_range in ranges[14:]:
                atr = (atr * 13 + true_range) / 14
        return {"sma20": sma, "relative_volume20": relative_volume, "atr14": atr}

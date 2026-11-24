"""Causal Decimal indicator series. Missing warm-up values are None."""

from datetime import timedelta
from decimal import Decimal, localcontext

from .calendar import IST

VERSION = "1"


def _average(values):
    return sum(values, Decimal(0)) / len(values)


def _smooth(values, period, alpha):
    seed = []
    previous = None
    for value in values:
        if value is None:
            yield None
            continue
        if previous is None:
            seed.append(value)
            if len(seed) == period:
                previous = _average(seed)
        else:
            previous += alpha * (value - previous)
        yield previous


def calculate(bars, *, sessions=None, benchmark=None):
    """Produce one value per observation, with no interpolation between series."""
    if len(bars) > 4000 or any(b.close_time <= a.close_time for a, b in zip(bars, bars[1:])):
        raise ValueError("Indicators require bounded, ordered OHLCV observations.")
    with localcontext() as context:
        context.prec = 28
        return _calculate(bars, sessions, benchmark)


def _calculate(bars, sessions, benchmark):
    closes = [bar.close for bar in bars]
    true_ranges, plus, minus, gains, losses = [[None] for _ in range(5)] if bars else [[] for _ in range(5)]
    for previous, bar in zip(bars, bars[1:]):
        true_ranges.append(max(bar.high - bar.low, abs(bar.high - previous.close), abs(bar.low - previous.close)))
        up, down = bar.high - previous.high, previous.low - bar.low
        plus.append(up if up > max(down, 0) else Decimal(0))
        minus.append(down if down > max(up, 0) else Decimal(0))
        move = bar.close - previous.close
        gains.append(max(move, Decimal(0)))
        losses.append(max(-move, Decimal(0)))
    wilder = Decimal(1) / 14
    atr = list(_smooth(true_ranges, 14, wilder))
    rsi = [None if gain is None else (100 * gain / (gain + loss) if gain + loss else Decimal(50))
           for gain, loss in zip(_smooth(gains, 14, wilder), _smooth(losses, 14, wilder))]
    directional = [
        None if positive is None else (100 * abs(positive - negative) / (positive + negative) if positive + negative else Decimal(0))
        for positive, negative in zip(_smooth(plus, 14, wilder), _smooth(minus, 14, wilder))
    ]
    ema12 = list(_smooth(closes, 12, Decimal(2) / 13))
    ema26 = list(_smooth(closes, 26, Decimal(2) / 27))
    macd = [fast - slow if slow is not None else None for fast, slow in zip(ema12, ema26)]
    signals = list(_smooth(macd, 9, Decimal(2) / 10))
    results = {"atr14": atr, "rsi14": rsi, "adx14": list(_smooth(directional, 14, wilder)),
               "ema20": list(_smooth(closes, 20, Decimal(2) / 21)),
               "macd": [None if line is None else (line, signal, line - signal if signal is not None else None)
                        for line, signal in zip(macd, signals)]}
    keys = ("sma20", "bollinger20", "stochastic14", "relative_volume20", "roc10", "obv",
            "volatility20", "high_low20", "opening_range15", "relative_strength", "gap",
            "volume_spike", "trend_slope20", "vwap")
    results.update({key: [] for key in keys})
    session_day = None
    total_value = obv = Decimal(0)
    total_volume = 0
    opening_high = opening_low = None
    opening_valid = True
    expected_open = None
    vwap_valid = False
    for index, bar in enumerate(bars):
        previous = bars[index - 1] if index else None
        start = bar.close_time.astimezone(IST).date()
        new_day = start != session_day
        session = sessions.get(start) if sessions else None
        if new_day:
            session_day, total_value, total_volume = start, Decimal(0), 0
            opening_high = opening_low = None
            expected_open = session.opening if session else None
            opening_valid = vwap_valid = expected_open is not None
        if bar.open_time is None or bar.open_time != expected_open:
            vwap_valid = False
        if session and session.opening is not None:
            end = session.opening + timedelta(minutes=15)
            if bar.open_time is not None and bar.open_time < end:
                opening_valid &= bar.open_time == expected_open and bar.close_time <= end
                opening_high = bar.high if opening_high is None else max(opening_high, bar.high)
                opening_low = bar.low if opening_low is None else min(opening_low, bar.low)
                if bar.close_time == end and opening_valid:
                    opening_range = (opening_high, opening_low)
                else:
                    opening_range = None
            else:
                opening_range = results["opening_range15"][-1] if index and not new_day else None
        else:
            opening_range = None
        expected_open = bar.close_time
        total_value += (bar.high + bar.low + bar.close) * bar.volume / 3
        total_volume += bar.volume
        if previous:
            obv += bar.volume if bar.close > previous.close else -bar.volume if bar.close < previous.close else 0
        mean = bands = slope = extrema = stoch = rel_volume = volatility = None
        if index >= 19:
            window = closes[index - 19:index + 1]
            mean = _average(window)
            std = _average([(close - mean) ** 2 for close in window]).sqrt()
            bands = (mean - 2 * std, mean, mean + 2 * std)
            slope = sum((Decimal(i) - Decimal("9.5")) * close for i, close in enumerate(window)) / 665
            extrema = (max(row.high for row in bars[index - 19:index + 1]), min(row.low for row in bars[index - 19:index + 1]))
        if index >= 13:
            window = bars[index - 13:index + 1]
            high, low = max(row.high for row in window), min(row.low for row in window)
            if high != low:
                stoch = 100 * (bar.close - low) / (high - low)
        if index >= 20:
            average_volume = _average([row.volume for row in bars[index - 20:index]])
            if average_volume:
                rel_volume = Decimal(bar.volume) / average_volume
            changes = [closes[j] / closes[j - 1] - 1 for j in range(index - 19, index + 1)]
            average_change = _average(changes)
            volatility = _average([(value - average_change) ** 2 for value in changes]).sqrt()
        aligned = benchmark.get(bar.close_time) if benchmark else None
        suitable_benchmark = (aligned and bar.available_at and aligned.available_at
                              and aligned.available_at <= bar.available_at and aligned.close > 0)
        values = (mean, bands, stoch, rel_volume, bar.close / closes[index - 10] - 1 if index >= 10 else None,
                  obv, volatility, extrema, opening_range,
                  bar.close / aligned.close if suitable_benchmark else None,
                  bar.open / previous.close - 1 if new_day and previous else None,
                  rel_volume >= 2 if rel_volume is not None else None,
                  slope, total_value / total_volume if total_volume and vwap_valid else None)
        for key, value in zip(keys, values):
            results[key].append(value)
    return results

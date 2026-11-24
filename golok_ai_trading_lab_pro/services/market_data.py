"""Version 1 close-time OHLCV import contract."""

import csv
import io
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal

VERSION = "1"
MAX_BYTES = 512 * 1024
MAX_ROWS = 4000
COLUMNS = ("close_time", "open", "high", "low", "close", "volume")
TEMPORAL_COLUMNS = (*COLUMNS, "open_time", "available_at")
INTERVALS = {"1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "1d": None}
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00(?:Z|[+-]\d{2}:\d{2})", re.ASCII)
NUMBER = re.compile(r"[0-9]{1,12}(?:\.[0-9]{1,8})?")
MAX_VOLUME = 2_147_483_647


@dataclass(frozen=True)
class Candle:
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    open_time: datetime | None = None
    available_at: datetime | None = None


def parse_timestamp(timestamp):
    if not TIMESTAMP.fullmatch(timestamp):
        raise ValueError("Use an ISO 8601 close timestamp with an explicit offset and zero seconds.")
    if not timestamp.endswith("Z") and (int(timestamp[-5:-3]) > 23 or int(timestamp[-2:]) > 59):
        raise ValueError("Invalid timestamp offset.")
    try:
        return datetime.fromisoformat(timestamp).astimezone(timezone.utc)
    except (ValueError, OverflowError):
        raise ValueError("Invalid close timestamp.") from None


def parse_bar(timestamp, open_, high, low, close, volume, *, as_of, open_time=None, available_at=None):
    close_time = parse_timestamp(timestamp)
    if close_time > as_of:
        raise ValueError("Future close timestamp.")
    values = (open_, high, low, close)
    if not all(NUMBER.fullmatch(value) for value in values):
        raise ValueError("Invalid price format or precision.")
    prices = tuple(Decimal(value) for value in values)
    opening, upper, lower, closing = prices
    if lower <= 0 or lower > min(opening, closing) or upper < max(opening, closing):
        raise ValueError("Invalid OHLC relationship.")
    if not re.fullmatch(r"[0-9]{1,10}", volume) or int(volume) > MAX_VOLUME:
        raise ValueError("Volume must be a nonnegative integer within the supported range.")
    if open_time is None and available_at is None:
        return Candle(close_time, *prices, int(volume))
    if not isinstance(open_time, str) or not isinstance(available_at, str):
        raise ValueError("Supply both open_time and available_at.")
    opening_time, availability = parse_timestamp(open_time), parse_timestamp(available_at)
    if not opening_time < close_time <= availability <= as_of:
        raise ValueError("Expected open_time < close_time <= available_at <= import time.")
    return Candle(close_time, *prices, int(volume), opening_time, availability)


def parse_csv(raw, *, as_of, temporal=False):
    if len(raw) > MAX_BYTES:
        raise ValueError("CSV file exceeds 512 KiB.")
    rows = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    try:
        columns = TEMPORAL_COLUMNS if temporal else COLUMNS
        if tuple(next(rows, ())) != columns:
            raise ValueError("Expected columns: " + ",".join(columns))
        bars = []
        for row in rows:
            try:
                if len(bars) >= MAX_ROWS:
                    raise ValueError("CSV file exceeds 4,000 candles.")
                if len(row) != len(columns):
                    raise ValueError(f"Expected exactly {len(columns)} columns.")
                temporal_values = dict(zip(columns[6:], row[6:]))
                bar = parse_bar(*row[:6], as_of=as_of, **temporal_values)
                if bars and bar.close_time <= bars[-1].close_time:
                    raise ValueError("Close times must be strictly increasing and unique.")
                bars.append(bar)
            except ValueError as exc:
                raise ValueError(f"CSV line {rows.line_num}: {exc}") from None
    except csv.Error:
        raise ValueError("Malformed CSV.") from None
    if not bars:
        raise ValueError("CSV contains no candle rows.")
    return bars


def check_series(bars, interval):
    """Return the number of breaks in an intraday series.

    Overnight and daily gaps need a verified exchange calendar.
    """
    seconds = INTERVALS[interval]
    if seconds is None:
        return 0
    india = timezone(timedelta(hours=5, minutes=30))
    return sum(
        end.close_time.astimezone(india).date() == start.close_time.astimezone(india).date()
        and (end.close_time - start.close_time).total_seconds() != seconds
        for start, end in zip(bars, bars[1:])
    )

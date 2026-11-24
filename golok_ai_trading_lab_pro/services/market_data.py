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


def parse_bar(timestamp, open_, high, low, close, volume, *, as_of):
    if not TIMESTAMP.fullmatch(timestamp):
        raise ValueError("Use an ISO 8601 close timestamp with an explicit offset and zero seconds.")
    try:
        close_time = datetime.fromisoformat(timestamp).astimezone(timezone.utc)
    except (ValueError, OverflowError):
        raise ValueError("Invalid close timestamp.") from None
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
    return Candle(close_time, *prices, int(volume))


def parse_csv(raw, *, as_of):
    if len(raw) > MAX_BYTES:
        raise ValueError("CSV file exceeds 512 KiB.")
    rows = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    try:
        if tuple(next(rows, ())) != COLUMNS:
            raise ValueError("Expected columns: " + ",".join(COLUMNS))
        bars = []
        for row in rows:
            try:
                if len(bars) >= MAX_ROWS:
                    raise ValueError("CSV file exceeds 4,000 candles.")
                if len(row) != len(COLUMNS):
                    raise ValueError("Expected exactly six columns.")
                bar = parse_bar(*row, as_of=as_of)
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

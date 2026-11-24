"""Normalize explicitly open-stamped provider history against a full session grid."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from . import market_data


def normalize(rows, session, seconds, received_at):
    if not isinstance(received_at, datetime) or received_at.utcoffset() is None:
        raise ValueError("The receipt clock is unavailable.")
    expected = session.slots(seconds)
    if not expected or len(rows) != len(expected):
        raise ValueError("The provider response does not cover the complete session grid.")
    bars = []
    for row, (opening, closing) in zip(rows, expected):
        event, *values = row
        if event != opening or closing > received_at:
            raise ValueError("The observed timestamps do not match a complete open-stamped session.")
        candle = market_data.parse_bar(
            closing.isoformat(), *[format(value, "f") if isinstance(value, Decimal) else str(value) for value in values],
            as_of=received_at,
        )
        # Receipt establishes when this application demonstrably had the information.
        # It does not establish when the vendor first published it.
        available = (received_at + timedelta(seconds=bool(received_at.microsecond))).replace(microsecond=0)
        bars.append(replace(candle, open_time=opening, available_at=available))
    return bars


def quote_freshness(event, receipt, max_age=timedelta(seconds=30)):
    if event is None or event > receipt:
        return "unknown"
    return "within_age_limit" if receipt - event <= max_age else "stale"


def parse_feed_time(value):
    # Offset-less provider strings require independently confirmed timezone semantics.
    if not isinstance(value, str) or len(value) > 40:
        return None
    try:
        event = datetime.fromisoformat(value)
    except ValueError:
        return None
    return event.astimezone(timezone.utc) if event.utcoffset() is not None else None

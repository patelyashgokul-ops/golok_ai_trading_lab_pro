"""Explicit, date-specific equity session calendars."""

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30), "IST")
UTC = timezone.utc
MAX_DAYS = 370
SLOTS = ("open", "close", "entry_cutoff", "exit_cutoff")


def _clock(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{2}:[0-9]{2}", value):
        raise ValueError("Session times must use HH:MM in Asia/Kolkata.")
    return time.fromisoformat(value)


@dataclass(frozen=True)
class Session:
    day: date
    kind: str
    opening: datetime | None = None
    closing: datetime | None = None
    entry_cutoff: datetime | None = None
    exit_cutoff: datetime | None = None
    pre_open: datetime | None = None

    def slots(self, seconds):
        if self.kind == "closed":
            return []
        if seconds is None:
            return [(self.opening, self.closing)]
        delta = timedelta(seconds=seconds)
        start = self.opening
        slots = []
        while start < self.closing:
            end = min(start + delta, self.closing)
            slots.append((start, end))
            start = end
        return slots


def load_schedule(raw):
    if not raw or len(raw) > 96 * 1024:
        raise ValueError("Supply a calendar JSON document up to 96 KiB.")
    try:
        rows = json.loads(raw)
    except (ValueError, RecursionError):
        raise ValueError("Calendar JSON is invalid.") from None
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_DAYS:
        raise ValueError("Supply 1–370 explicit calendar dates.")
    sessions = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("date"), str):
            raise ValueError("Each calendar row needs an ISO trading date.")
        day = date.fromisoformat(row["date"])
        if day.isoformat() != row["date"] or day in sessions:
            raise ValueError("Calendar dates must be canonical and unique.")
        kind = row.get("kind")
        if kind == "closed" and set(row) == {"date", "kind"}:
            sessions[day] = Session(day, kind)
            continue
        keys = {"date", "kind", *SLOTS}
        if kind not in ("regular", "special") or set(row) not in (keys, keys | {"pre_open"}):
            raise ValueError("Trading days need opening, closing, entry and exit times.")
        times = [datetime.combine(day, _clock(row[key]), IST).astimezone(UTC) for key in SLOTS]
        opening, closing, entry, exit_ = times
        if not opening < entry <= exit_ <= closing:
            raise ValueError("Expected opening < entry cutoff <= exit cutoff <= closing.")
        pre_open = datetime.combine(day, _clock(row["pre_open"]), IST).astimezone(UTC) if "pre_open" in row else None
        if pre_open is not None and pre_open >= opening:
            raise ValueError("Pre-open must precede continuous trading.")
        sessions[day] = Session(day, kind, *times, pre_open)
    return sessions


def validate_bar(bar, sessions, seconds):
    day = bar.close_time.astimezone(IST).date()
    session = sessions.get(day)
    if session is None or session.kind == "closed":
        raise ValueError(f"No eligible continuous trading session on {day}.")
    if bar.open_time is None or bar.available_at is None:
        raise ValueError("Calendar datasets require open_time and available_at.")
    elapsed = (bar.open_time - session.opening).total_seconds()
    expected_close = min(bar.open_time + timedelta(seconds=seconds), session.closing) if seconds else session.closing
    if (elapsed < 0 or bar.open_time >= session.closing or bar.close_time != expected_close
            or (elapsed % seconds if seconds else elapsed)):
        raise ValueError(f"Candle is outside the session grid on {day}.")
    return session


def missing_observations(bars, sessions, seconds):
    """Count missing grid positions between the first and last observed close."""
    if not bars:
        return 0
    first, last = bars[0].close_time, bars[-1].close_time
    current = first.astimezone(IST).date()
    end = last.astimezone(IST).date()
    observed = {bar.close_time for bar in bars}
    if (end - current).days >= MAX_DAYS:
        raise ValueError("Calendar coverage is incomplete for the selected window.")
    missing = 0
    while current <= end:
        session = sessions.get(current)
        if session is None:
            raise ValueError(f"Calendar coverage is incomplete on {current}.")
        missing += sum(first <= close <= last and close not in observed for _, close in session.slots(seconds))
        current += timedelta(days=1)
    return missing

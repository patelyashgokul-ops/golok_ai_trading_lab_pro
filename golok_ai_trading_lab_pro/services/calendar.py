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
    segments: tuple = ()
    post_close: datetime | None = None

    def windows(self):
        if self.kind == "closed":
            return ()
        return self.segments or ((self.opening, self.closing),)

    def slots(self, seconds):
        windows = self.windows()
        if seconds is None:
            return list(windows) if len(windows) == 1 else []
        if type(seconds) is not int or seconds < 60:
            raise ValueError("The session grid requires an interval of at least one minute.")
        delta = timedelta(seconds=seconds)
        slots = []
        for start, closing in windows:
            while start < closing:
                end = min(start + delta, closing)
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
        if kind not in ("regular", "special") or not keys <= row.keys() <= keys | {"pre_open", "segments", "post_close"}:
            raise ValueError("Trading days need opening, closing, entry and exit times.")
        times = [datetime.combine(day, _clock(row[key]), IST).astimezone(UTC) for key in SLOTS]
        opening, closing, entry, exit_ = times
        if not opening < entry <= exit_ <= closing:
            raise ValueError("Expected opening < entry cutoff <= exit cutoff <= closing.")
        pre_open = datetime.combine(day, _clock(row["pre_open"]), IST).astimezone(UTC) if "pre_open" in row else None
        if pre_open is not None and pre_open >= opening:
            raise ValueError("Pre-open must precede continuous trading.")
        post_close = datetime.combine(day, _clock(row["post_close"]), IST).astimezone(UTC) if "post_close" in row else None
        if post_close is not None and post_close <= closing:
            raise ValueError("Post-close period must follow continuous trading.")
        segments = []
        if "segments" in row:
            entries = row["segments"]
            if not isinstance(entries, list) or not 2 <= len(entries) <= 8:
                raise ValueError("Supply 2–8 segments for split sessions.")
            for span in entries:
                if not isinstance(span, list) or len(span) != 2:
                    raise ValueError("A segment needs opening and closing times.")
                left, right = [datetime.combine(day, _clock(value), IST).astimezone(UTC) for value in span]
                if not opening <= left < right <= closing or (segments and left <= segments[-1][1]):
                    raise ValueError("Segments must be ordered with distinct continuous windows.")
                segments.append((left, right))
            if segments[0][0] != opening or segments[-1][1] != closing:
                raise ValueError("The segments must span the stated session bounds.")
            if not any(left < entry <= right for left, right in segments) or not any(left < exit_ <= right for left, right in segments):
                raise ValueError("Entry and exit cutoffs must be in continuous trading.")
        sessions[day] = Session(day, kind, *times, pre_open, tuple(segments), post_close)
    return sessions


def validate_bar(bar, sessions, seconds):
    day = bar.close_time.astimezone(IST).date()
    session = sessions.get(day)
    if session is None or session.kind == "closed":
        raise ValueError(f"No eligible continuous trading session on {day}.")
    if bar.open_time is None or bar.available_at is None:
        raise ValueError("Calendar datasets require open_time and available_at.")
    if bar.available_at < bar.close_time:
        raise ValueError("A completed candle cannot be published before its close.")
    if seconds is None:
        if (bar.open_time, bar.close_time) in session.slots(None):
            return session
    elif type(seconds) is int and seconds >= 60:
        for opening, closing in session.windows():
            elapsed = (bar.open_time - opening).total_seconds()
            if (opening <= bar.open_time < closing and elapsed % seconds == 0
                    and bar.close_time == min(bar.open_time + timedelta(seconds=seconds), closing)):
                return session
    raise ValueError(f"Candle is outside the session grid on {day}.")


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

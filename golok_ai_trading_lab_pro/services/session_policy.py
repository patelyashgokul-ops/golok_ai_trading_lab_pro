"""Local lifetime and fresh operator authorization for read-only broker sessions."""

import re
from datetime import datetime, time, timedelta

from .calendar import IST

MAX_AGE = timedelta(minutes=30)
MAX_TOTP_AGE = timedelta(seconds=25)


def deadline(now):
    local = now.astimezone(IST)
    midnight = datetime.combine(local.date() + timedelta(days=1), time.min, IST)
    return min(now + MAX_AGE, midnight)


def fresh(code, issued_at, now):
    if (not isinstance(code, str) or not re.fullmatch(r"[0-9]{6}", code)
            or not isinstance(issued_at, str) or len(issued_at) > 35):
        return False
    try:
        issued = datetime.fromisoformat(issued_at)
        return issued.utcoffset() is not None and timedelta(0) <= now - issued <= MAX_TOTP_AGE
    except (TypeError, ValueError, OverflowError):
        return False

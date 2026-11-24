"""Bounded Upstox V3 historical cash-equity reader."""

import json
import re
from datetime import datetime, timezone
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from . import calendar, market_data
from .smartapi import ProviderError

HOST = "https://api.upstox.com"
MAX_BODY = 256 * 1024
INTERVALS = frozenset({"1m", "3m", "5m", "15m"})


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, newurl):
        return None


def _https(path, token):
    request = Request(HOST + path, headers={
        "Authorization": "Bearer " + token, "Accept": "application/json",
    }, method="GET")
    with build_opener(NoRedirect()).open(request, timeout=7) as response:
        return response.read(MAX_BODY + 1)


def identity(exchange, key, isin):
    return (exchange == "NSE" and isinstance(isin, str)
            and re.fullmatch(r"IN[A-Z0-9]{9}[0-9]", isin) is not None
            and key == "NSE_EQ|" + isin)


def history(token, key, isin, interval, session, reserve, *, transport=_https):
    if not isinstance(token, str) or not re.fullmatch(r"[A-Za-z0-9._~+/=-]{1,4096}", token):
        raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
    if not identity("NSE", key, isin) or interval not in INTERVALS:
        raise ProviderError("DEGRADED")
    day = session.opening.astimezone(calendar.IST).date()
    if session.closing.astimezone(calendar.IST).date() != day or session.closing > datetime.now(timezone.utc):
        raise ProviderError("DEGRADED")
    if not reserve("upstox_history"):
        raise ProviderError("RATE_LIMITED")
    path = f"/v3/historical-candle/{quote(key, safe='')}/minutes/{interval[:-1]}/{day}/{day}"
    try:
        payload = transport(path, token)
    except HTTPError as exc:
        exc.close()
        if exc.code in (401, 403):
            raise ProviderError("AUTH_REQUIRED") from None
        if exc.code == 429:
            raise ProviderError("RATE_LIMITED") from None
        raise ProviderError("DISCONNECTED" if 500 <= exc.code <= 599 else "DEGRADED") from None
    except (URLError, OSError):
        raise ProviderError("DISCONNECTED") from None
    receipt = datetime.now(timezone.utc)
    try:
        if not isinstance(payload, bytes) or len(payload) > MAX_BODY:
            raise ValueError
        result = json.loads(payload, parse_float=Decimal)
        if result["status"] != "success":
            raise ValueError
        raw = result["data"]["candles"]
        expected = session.slots(market_data.INTERVALS[interval])
        if not isinstance(raw, list) or not expected or len(raw) != len(expected):
            raise ValueError
        bars = []
        for row in raw:
            if (not isinstance(row, list) or len(row) != 7
                    or any(type(value) not in (int, Decimal) for value in row[1:5])
                    or any(type(value) is not int or value < 0 for value in row[5:])):
                raise ValueError
            prices = [format(value, "f") for value in row[1:5]]
            bar = market_data.parse_bar(row[0], *prices, str(row[5]), as_of=receipt)
            bars.append((bar.close_time, bar.open, bar.high, bar.low, bar.close, bar.volume))
        return tuple(sorted(bars, key=lambda row: row[0])), receipt
    except (KeyError, TypeError, ValueError, ArithmeticError, RecursionError, AttributeError):
        raise ProviderError("DEGRADED") from None

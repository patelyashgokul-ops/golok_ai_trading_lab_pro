"""Read-only Upstox cash-equity REST and V3 LTPC stream adapters."""

import gzip
import io
import json
import re
import struct
from contextlib import closing
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import ProxyHandler, build_opener
from uuid import uuid4

from . import upstox
from .smartapi import ProviderError

MASTER_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
MASTER_COMPRESSED = 12 * 1024 * 1024
MASTER_BYTES = 64 * 1024 * 1024
MAX_AGE = timedelta(seconds=30)


def _get(token, operation, path, reserve, transport):
    if not upstox.credential_present(token):
        raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
    if not reserve(operation):
        raise ProviderError("RATE_LIMITED")
    try:
        payload = transport(path, token)
        if not isinstance(payload, bytes) or len(payload) > upstox.MAX_BODY:
            raise ValueError
        result = json.loads(payload, parse_float=Decimal)
        if result["status"] != "success" or not isinstance(result["data"], dict):
            raise ValueError
        return result["data"]
    except HTTPError as exc:
        exc.close()
        code = {401: "AUTH_REQUIRED", 403: "AUTH_REQUIRED", 429: "RATE_LIMITED"}.get(exc.code)
        raise ProviderError(code or ("DISCONNECTED" if exc.code >= 500 else "DEGRADED")) from None
    except (URLError, OSError):
        raise ProviderError("DISCONNECTED") from None
    except (KeyError, TypeError, ValueError, RecursionError):
        raise ProviderError("DEGRADED") from None


def _price(value):
    value = Decimal(str(value))
    if not value.is_finite() or not 0 < value < 10**12:
        raise ValueError
    return value


def quote_snapshot(token, key, isin, reserve, *, transport=upstox._https):
    if not upstox.identity("NSE", key, isin):
        raise ProviderError("DEGRADED")
    path = f"/v3/market-quote/ltp?instrument_key={quote(key, safe='')}"
    data = _get(token, "upstox_quote", path, reserve, transport)
    try:
        item, = data.values()
        if item["instrument_token"] != key or type(item["last_price"]) not in (int, Decimal):
            raise ValueError
        # The LTP V3 response has no exchange event timestamp.
        return {"price": str(_price(item["last_price"])), "freshness": "UNKNOWN"}
    except (KeyError, TypeError, ValueError, ArithmeticError):
        raise ProviderError("DEGRADED") from None


def _master_file():
    with build_opener(ProxyHandler({}), upstox.NoRedirect()).open(MASTER_URL, timeout=8) as response:
        return response.read(MASTER_COMPRESSED + 1)


def instrument_master(reserve, *, transport=_master_file):
    if not reserve("upstox_master"):
        raise ProviderError("RATE_LIMITED")
    try:
        data = transport()
        if not isinstance(data, bytes) or len(data) > MASTER_COMPRESSED:
            raise ValueError
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as source:
            raw = source.read(MASTER_BYTES + 1)
        if len(raw) > MASTER_BYTES:
            raise ValueError
        entries = json.loads(raw, parse_float=Decimal)
        if not isinstance(entries, list) or len(entries) > 300_000:
            raise ValueError
        matched = {}
        for item in entries:
            if item.get("segment") != "NSE_EQ" or item.get("instrument_type") != "EQ":
                continue
            key, isin, symbol = item["instrument_key"], item["isin"], item["trading_symbol"]
            if (not upstox.identity("NSE", key, isin) or key in matched
                    or not re.fullmatch(r"[A-Z0-9][A-Z0-9&._-]{0,30}", symbol)
                    or type(item["lot_size"]) is not int or not 0 < item["lot_size"] <= 10_000):
                raise ValueError
            matched[key] = {"isin": isin, "symbol": symbol, "lot": item["lot_size"]}
        if not matched:
            raise ValueError
        return matched
    except (KeyError, AttributeError, TypeError, ValueError, OSError, EOFError, RecursionError):
        raise ProviderError("DEGRADED") from None


def _varint(raw, pos):
    value = 0
    for shift in range(0, 70, 7):
        byte = raw[pos]
        pos += 1
        value |= (byte & 127) << shift
        if byte < 128 and value < 2**64:
            return value, pos
    raise ValueError


def _fields(raw):
    pos = 0
    while pos < len(raw):
        tag, pos = _varint(raw, pos)
        number, wire = divmod(tag, 8)
        if not number or wire not in (0, 1, 2, 5):
            raise ValueError
        if wire == 0:
            value, pos = _varint(raw, pos)
        else:
            size, pos = _varint(raw, pos) if wire == 2 else (8 if wire == 1 else 4, pos)
            if pos + size > len(raw):
                raise ValueError
            value = raw[pos:pos + size]
            pos += size
        yield number, value


def _millis(value):
    if type(value) is not int or not 0 < value < 4_102_444_800_000:
        raise ValueError
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=value)


def decode_ltpc(raw, key, receipt, market_open=False):
    """Decode only the documented V3 LTPC subscription fields."""
    try:
        if not isinstance(raw, bytes) or not 0 < len(raw) <= upstox.MAX_BODY:
            raise ValueError
        fields = list(_fields(raw))
        header = dict(fields)
        kind = header.get(1, 0)
        if kind == 2:
            statuses = (dict(_fields(entry)) for number, entry in _fields(header[4]) if number == 1)
            return any(entry.get(1) == b"NSE_EQ" and entry.get(2) == 2 for entry in statuses), None
        if kind != 1 or not market_open:
            return market_open, None
        published = _millis(header[3])
        for number, entry in fields:
            if number != 2:
                continue
            mapped = dict(_fields(entry))
            if mapped.get(1) != key.encode("ascii"):
                continue
            values = dict(_fields(dict(_fields(mapped[2]))[1]))
            event = _millis(values[2])
            if not event <= published <= receipt or receipt - event > MAX_AGE:
                return market_open, None
            price = _price(struct.unpack("<d", values[1])[0])
            return market_open, {"price": str(price), "event": event, "published": published, "receipt": receipt}
        return market_open, None
    except (IndexError, KeyError, TypeError, ValueError, OverflowError, ArithmeticError, struct.error):
        raise ProviderError("DEGRADED") from None


def _connect(uri):
    try:
        import websocket
    except ImportError:
        raise ProviderError("STREAM_DEPENDENCY_REQUIRED") from None
    try:
        return websocket.create_connection(uri, timeout=3, redirect_limit=0, http_no_proxy=["*"])
    except (OSError, websocket.WebSocketException):
        raise ProviderError("DISCONNECTED") from None


def stream_updates(token, key, isin, reserve, *, active=lambda: True, duration=180, max_frames=120_000,
                   transport=upstox._https, connect=_connect, clock=lambda: datetime.now(timezone.utc)):
    if not upstox.identity("NSE", key, isin):
        raise ProviderError("DEGRADED")
    result = _get(token, "upstox_stream", "/v3/feed/market-data-feed/authorize", reserve, transport)
    try:
        uri = result["authorized_redirect_uri"]
        location = urlsplit(uri)
        if (len(uri) > 2048 or location.scheme != "wss" or not location.hostname.endswith(".upstox.com")
                or location.port not in (None, 443) or location.username or location.password or location.fragment
                or location.path != "/market-data-feeder/v3/upstox-developer-api/feeds" or not location.query):
            raise ValueError
    except (AttributeError, KeyError, ValueError, TypeError):
        raise ProviderError("DEGRADED") from None
    stream = connect(uri)
    try:
        try:
            stream.send_binary(json.dumps({"guid": str(uuid4()), "method": "sub",
                                           "data": {"mode": "ltpc", "instrumentKeys": [key]}}).encode())
        except Exception:
            raise ProviderError("DISCONNECTED") from None
        opened, deadline = False, monotonic() + duration
        for _ in range(max_frames):
            if monotonic() >= deadline or not active():
                break
            try:
                frame = stream.recv()
            except Exception as exc:
                if isinstance(exc, TimeoutError) or type(exc).__name__ == "WebSocketTimeoutException":
                    continue
                raise ProviderError("DISCONNECTED") from None
            if frame in ("", b""):
                raise ProviderError("DISCONNECTED")
            opened, sample = decode_ltpc(frame, key, clock(), opened)
            if sample:
                yield sample
    finally:
        try:
            stream.close(timeout=0)
        except Exception:
            pass


def stream_sample(token, key, isin, reserve, *, transport=upstox._https, connect=_connect,
                  clock=lambda: datetime.now(timezone.utc)):
    updates = stream_updates(token, key, isin, reserve, duration=8, max_frames=12,
                             transport=transport, connect=connect, clock=clock)
    with closing(updates):
        return next(updates, None)

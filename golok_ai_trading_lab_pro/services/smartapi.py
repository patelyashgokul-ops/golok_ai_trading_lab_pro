"""Narrow SmartAPI REST client. Session state is process-local."""

import json
import os
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from . import market_data
from .ingestion import parse_feed_time, quote_freshness

HOST = "https://apiconnect.angelone.in"
ENDPOINTS = {
    "authenticate": "/rest/auth/angelbroking/user/v1/loginByPassword",
    "history": "/rest/secure/angelbroking/historical/v1/getCandleData",
    "quote": "/rest/secure/angelbroking/market/v1/quote",
}
CAPABILITIES = frozenset(ENDPOINTS)
INTERVALS = dict(zip(market_data.INTERVALS, (
    "ONE_MINUTE", "THREE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE",
    "THIRTY_MINUTE", "ONE_HOUR", "ONE_DAY",
)))
MAX_BODY = 512 * 1024


class ProviderError(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _https(operation, headers, payload, timeout):
    if operation not in ENDPOINTS:
        raise ProviderError("Unsupported provider operation.")
    # Do not forward authentication headers to a redirect or ambient HTTP proxy.
    opener = build_opener(ProxyHandler({}), NoRedirect())
    request = Request(HOST + ENDPOINTS[operation], data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_BODY + 1)
        if len(raw) > MAX_BODY:
            raise ProviderError("Provider response exceeds the permitted size.")
        return json.loads(raw, parse_float=Decimal)
    except HTTPError as exc:
        reason = "RATE_LIMITED" if exc.code == 429 else "AUTH_REQUIRED" if exc.code == 401 else "DEGRADED"
        raise ProviderError(reason) from None
    except (TimeoutError, URLError, OSError):
        raise ProviderError("DISCONNECTED") from None
    except (UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, ProviderError):
            raise
        raise ProviderError("Invalid provider response.") from None


class SmartAPI:
    def __init__(self, transport=None, *, clock=monotonic, quota=None):
        self._transport = transport
        self._clock = clock
        self._headers = {}
        self._token = None
        self._next_request = 0
        self._calls = 0
        self._quota = quota
        self.state = "NOT_CONFIGURED" if transport is None else "AUTH_REQUIRED"
        self.last_success = None

    @classmethod
    def from_environment(cls):
        if os.environ.get("GOLOK_SMARTAPI_AUTHORIZED") != "1":
            return cls()
        key = os.environ.get("GOLOK_SMARTAPI_KEY")
        public_ip = os.environ.get("GOLOK_SMARTAPI_PUBLIC_IP")
        local_ip = os.environ.get("GOLOK_SMARTAPI_LOCAL_IP")
        mac = os.environ.get("GOLOK_SMARTAPI_MAC")
        if not all((key, public_ip, local_ip, mac)):
            return cls()
        from ipaddress import IPv4Address
        try:
            public_ip, local_ip = str(IPv4Address(public_ip)), str(IPv4Address(local_ip))
        except ValueError:
            raise ProviderError("Invalid SmartAPI network configuration.") from None
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", key) or not re.fullmatch(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac):
            raise ProviderError("Invalid SmartAPI configuration.")
        client = cls(_https)
        client._headers = {"X-PrivateKey": key, "X-ClientPublicIP": public_ip, "X-ClientLocalIP": local_ip,
                           "X-MACAddress": mac, "X-UserType": "USER", "X-SourceID": "WEB"}
        return client

    def _request(self, operation, payload):
        if operation not in CAPABILITIES:
            raise ProviderError("Unsupported provider operation.")
        if self._transport is None:
            raise ProviderError("NOT_CONFIGURED")
        if operation != "authenticate" and not self._token:
            raise ProviderError("AUTH_REQUIRED")
        now = self._clock()
        # Local caps, not provider limits. A client has a finite lifetime budget.
        if now < self._next_request or self._calls >= 30:
            self.state = "RATE_LIMITED"
            raise ProviderError(self.state)
        if self._quota and not self._quota(operation):
            self.state = "RATE_LIMITED"
            raise ProviderError(self.state)
        self._calls += 1
        self._next_request = now + 5
        headers = {**self._headers, "Content-Type": "application/json", "Accept": "application/json"}
        if operation != "authenticate":
            headers["Authorization"] = "Bearer " + self._token
        try:
            response = self._transport(operation, headers, payload, 7)
        except (ProviderError, TimeoutError, OSError) as exc:
            code = str(exc) if isinstance(exc, ProviderError) else "DISCONNECTED"
            self.state = code if code in {"RATE_LIMITED", "AUTH_REQUIRED", "DISCONNECTED"} else "DEGRADED"
            if self.state == "RATE_LIMITED":
                self._next_request = now + 60
            if self.state == "AUTH_REQUIRED":
                self._token = None
            raise ProviderError(self.state) from None
        if not isinstance(response, dict) or response.get("status") is not True or "data" not in response:
            code = response.get("errorcode") if isinstance(response, dict) else None
            if code == "AB1021":
                self._next_request = now + 60
                self.state = "RATE_LIMITED"
            elif operation == "authenticate" or code in ("AG8001", "AG8002", "AG8003"):
                self._token = None
                self.state = "AUTH_REQUIRED"
            else:
                self.state = "DEGRADED"
            raise ProviderError(self.state)
        return response["data"]

    def _success(self):
        self.state = "CONNECTED"
        self.last_success = datetime.now(timezone.utc)

    def _invalid(self):
        self.state = "DEGRADED"
        raise ProviderError("Invalid provider response.")

    def authenticate(self, client_code, pin, totp):
        self._token = None
        if not all(isinstance(value, str) and value for value in (client_code, pin, totp)):
            raise ProviderError("Authentication inputs are incomplete.")
        result = self._request("authenticate", {"clientcode": client_code, "password": pin, "totp": totp})
        jwt = result.get("jwtToken") if isinstance(result, dict) else None
        if not isinstance(jwt, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,4096}", jwt):
            self._invalid()
        self._token = jwt
        self._success()

    @staticmethod
    def _identity(exchange, token):
        if exchange not in ("NSE", "BSE") or not isinstance(token, str) or not re.fullmatch(r"[0-9]{1,20}", token):
            raise ProviderError("Invalid equity market identifier.")

    def history(self, exchange, token, interval, start, end):
        self._identity(exchange, token)
        if interval not in INTERVALS or not all(isinstance(value, datetime) and value.utcoffset() is not None for value in (start, end)):
            raise ProviderError("Historical request needs a supported interval and offset-aware boundaries.")
        if not timedelta(0) <= end - start <= timedelta(days=1):
            raise ProviderError("The local request cap is one day.")
        ist = timezone(timedelta(hours=5, minutes=30))
        data = self._request("history", {
            "exchange": exchange, "symboltoken": token, "interval": INTERVALS[interval],
            "fromdate": start.astimezone(ist).strftime("%Y-%m-%d %H:%M"),
            "todate": end.astimezone(ist).strftime("%Y-%m-%d %H:%M"),
        })
        if not isinstance(data, list) or len(data) > 1500:
            self._invalid()
        validated = []
        for row in data:
            try:
                if not isinstance(row, list) or len(row) != 6:
                    raise ValueError
                observation = market_data.parse_bar(str(row[0]), *map(str, row[1:]), as_of=end)
                if observation.close_time < start or (validated and observation.close_time <= validated[-1][0]):
                    raise ValueError
            except (ValueError, TypeError):
                self._invalid()
            # Broker row timestamp stays an event timestamp until semantics are verified.
            validated.append((observation.close_time, observation.open, observation.high,
                              observation.low, observation.close, observation.volume))
        self._success()
        return tuple(validated)

    def quote(self, exchange, token, *, full=False):
        self._identity(exchange, token)
        data = self._request("quote", {"mode": "FULL" if full else "LTP", "exchangeTokens": {exchange: [token]}})
        try:
            fetched = data["fetched"]
            if not isinstance(fetched, list) or len(fetched) != 1:
                raise ValueError
            result = fetched[0]
            price = Decimal(str(result["ltp"]))
            if result["exchange"] != exchange or str(result["symbolToken"]) != token or not price.is_finite() or price <= 0:
                raise ValueError
        except (KeyError, IndexError, TypeError, ValueError, InvalidOperation):
            self._invalid()
        self._success()
        event = parse_feed_time(result.get("exchFeedTime")) if full else None
        return {"exchange": exchange, "token": token, "price": price, "received_at": self.last_success,
                "event_at": event, "freshness": quote_freshness(event, self.last_success)}

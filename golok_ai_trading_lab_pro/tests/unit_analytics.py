import gzip
import json
import struct
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from services import local_secrets, upstox_analytics
from services.smartapi import ProviderError


KEY = "NSE_EQ|IN0000000001"
ISIN = "IN0000000001"
AUTHORED = "authored-fixture-only"


def varint(value):
    result = bytearray()
    while value >= 128:
        result.append(value & 127 | 128)
        value >>= 7
    return bytes(result + bytearray([value]))


def chunk(number, value):
    return varint(number * 8 + 2) + varint(len(value)) + value


def number(field, value):
    return varint(field * 8) + varint(value)


class AnalyticsAdapterTests(unittest.TestCase):
    def test_quote_matches_identity_and_keeps_exchange_clock_unknown(self):
        def transport(path, _credential):
            self.assertEqual(path, "/v3/market-quote/ltp?instrument_key=NSE_EQ%7CIN0000000001")
            return json.dumps({"status": "success", "data": {"NSE_EQ:FIXTURE": {
                "instrument_token": KEY, "last_price": 101.25,
            }}}).encode()

        self.assertEqual(upstox_analytics.quote_snapshot(AUTHORED, KEY, ISIN, lambda op: op == "upstox_quote",
                                                         transport=transport),
                         {"price": "101.25", "freshness": "UNKNOWN"})
        with self.assertRaisesRegex(ProviderError, "RATE_LIMITED"):
            upstox_analytics.quote_snapshot(AUTHORED, KEY, ISIN, lambda _op: False,
                                            transport=lambda *_args: self.fail("blocked quote used transport"))

    def test_stream_order_freshness_and_binary_subscription(self):
        now = datetime(2024, 1, 2, 4, tzinfo=timezone.utc)
        stamp = int(now.timestamp() * 1000)
        market = number(1, 2) + chunk(4, chunk(1, chunk(1, b"NSE_EQ") + number(2, 2)))
        price = b"\x09" + struct.pack("<d", 101.25) + number(2, stamp - 1000)
        payload = chunk(2, chunk(1, KEY.encode()) + chunk(2, chunk(1, price))) + number(3, stamp)
        self.assertEqual(upstox_analytics.decode_ltpc(market, KEY, now), (True, None))
        self.assertEqual(upstox_analytics.decode_ltpc(payload, KEY, now, True), (True, None))
        self.assertEqual(upstox_analytics.decode_ltpc(number(1, 1) + payload, KEY, now + timedelta(minutes=1), True),
                         (True, None))
        self.assertEqual(upstox_analytics.decode_ltpc(number(1, 1) + payload, KEY, now, False), (False, None))
        socket = Mock()
        socket.recv.side_effect = [market, payload, number(1, 1) + payload]
        uri = "wss://feed.upstox.com/market-data-feeder/v3/upstox-developer-api/feeds?code=synthetic"

        def transport(path, _credential):
            self.assertEqual(path, "/v3/feed/market-data-feed/authorize")
            return json.dumps({"status": "success", "data": {"authorized_redirect_uri": uri}}).encode()

        result = upstox_analytics.stream_sample(AUTHORED, KEY, ISIN, lambda op: op == "upstox_stream",
                                                transport=transport, connect=lambda _uri: socket, clock=lambda: now)
        self.assertEqual((result["price"], result["event"], result["published"]), ("101.25", now - timedelta(seconds=1), now))
        self.assertEqual(json.loads(socket.send_binary.call_args.args[0])["data"]["instrumentKeys"], [KEY])
        socket.close.assert_called_once()
        uri = uri.replace("feed.upstox.com", "feed.upstox.com.example.test")
        with self.assertRaisesRegex(ProviderError, "DEGRADED"):
            upstox_analytics.stream_sample(AUTHORED, KEY, ISIN, lambda _op: True, transport=transport,
                                           connect=lambda _uri: self.fail("untrusted redirect reached socket"))

    def test_master_keys_and_duplicate_rejection(self):
        item = {"segment": "NSE_EQ", "instrument_type": "EQ", "instrument_key": KEY, "isin": ISIN,
                "trading_symbol": "FIXTURE", "lot_size": 1}
        def data(rows):
            return gzip.compress(json.dumps(rows).encode())
        self.assertEqual(upstox_analytics.instrument_master(lambda _op: True, transport=lambda: data([item]))[KEY],
                         {"isin": ISIN, "symbol": "FIXTURE", "lot": 1})
        with self.assertRaisesRegex(ProviderError, "DEGRADED"):
            upstox_analytics.instrument_master(lambda _op: True, transport=lambda: data([item, item]))

    def test_continuous_window_keeps_socket_across_idle_timeout_and_stops_on_gate(self):
        now = datetime(2024, 1, 2, 4, tzinfo=timezone.utc)
        stamp = int(now.timestamp() * 1000)
        market = number(1, 2) + chunk(4, chunk(1, chunk(1, b"NSE_EQ") + number(2, 2)))

        def tick(value):
            ltpc = b"\x09" + struct.pack("<d", value) + number(2, stamp - 1000)
            return number(1, 1) + chunk(2, chunk(1, KEY.encode()) + chunk(2, chunk(1, ltpc))) + number(3, stamp)

        socket = Mock()
        socket.recv.side_effect = [market, tick(100), TimeoutError(), tick(101)]
        connect = Mock(return_value=socket)
        uri = "wss://feed.upstox.com/market-data-feeder/v3/upstox-developer-api/feeds?code=authored"
        transport = Mock(return_value=json.dumps({"status": "success", "data": {"authorized_redirect_uri": uri}}).encode())
        active = Mock(side_effect=[True, True, True, True, False])
        samples = list(upstox_analytics.stream_updates(
            AUTHORED, KEY, ISIN, lambda _op: True, transport=transport, connect=connect, clock=lambda: now, active=active))
        self.assertEqual([item["price"] for item in samples], ["100.0", "101.0"])
        connect.assert_called_once_with(uri)
        socket.close.assert_called_once()

    @unittest.skipUnless(sys.platform == "win32", "Windows-local vault")
    def test_windows_vault_binds_the_ciphertext(self):
        envelope = local_secrets.seal(AUTHORED, b"company:fixture")
        self.assertNotIn(AUTHORED, envelope)
        self.assertEqual(local_secrets.open_secret(envelope, b"company:fixture"), AUTHORED)
        with self.assertRaises(local_secrets.VaultError):
            local_secrets.open_secret(envelope, b"company:other")

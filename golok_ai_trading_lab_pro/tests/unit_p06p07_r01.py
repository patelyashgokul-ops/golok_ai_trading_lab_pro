import json
import unittest
from urllib.error import HTTPError, URLError

from services import calendar, ingestion, providers, upstox
from services.smartapi import ProviderError


class UpstoxTest(unittest.TestCase):
    key = "NSE_EQ|IN0000000001"
    isin = "IN0000000001"
    token = "authored-test-value"
    rows = [["2024-01-02T09:20:00+05:30", 100.05, 103, 99, 101, 20, 0],
            ["2024-01-02T09:15:00+05:30", 100, 103, 99, 100, 10, 0]]

    def setUp(self):
        self.session = next(iter(calendar.load_schedule(json.dumps([{
            "date": "2024-01-02", "kind": "regular", "open": "09:15", "close": "09:25",
            "entry_cutoff": "09:20", "exit_cutoff": "09:25",
        }])).values()))

    def read(self, transport, **changes):
        return upstox.history(**{
            "token": self.token, "key": self.key, "isin": self.isin, "interval": "5m",
            "session": self.session, "reserve": lambda op: op == "upstox_history",
            "transport": transport, **changes,
        })

    @staticmethod
    def payload(rows):
        return json.dumps({"status": "success", "data": {"candles": rows}}).encode()

    def test_ascending_normalization_and_receipt_provenance(self):
        def transport(path, token):
            self.assertEqual(path, "/v3/historical-candle/NSE_EQ%7CIN0000000001/minutes/5/2024-01-02/2024-01-02")
            self.assertEqual(token, self.token)
            return self.payload(self.rows)

        raw, receipt = self.read(transport)
        bars = ingestion.normalize(raw, self.session, 300, receipt)
        self.assertEqual(bars[0].open_time, self.session.opening)
        self.assertEqual(bars[-1].close_time, self.session.closing)
        self.assertEqual(str(bars[-1].open), "100.05")
        self.assertGreaterEqual(bars[-1].available_at, receipt)

    def test_schema_grid_and_values(self):
        bad_rows = ([], self.rows[:1], [self.rows[0], self.rows[0]],
                    [self.rows[0], ["2024-01-02T09:16:00+05:30", *self.rows[1][1:]]])
        for rows in bad_rows:
            with self.subTest(rows=rows), self.assertRaises((ValueError, ProviderError)):
                raw, receipt = self.read(lambda *_: self.payload(rows))
                ingestion.normalize(raw, self.session, 300, receipt)
        for body in (b"<html>invalid</html>", b" " * (upstox.MAX_BODY + 1),
                     self.payload([self.rows[0], [self.rows[1][0], 100, 90, 99, 100, 10, 0]]),
                     self.payload([self.rows[0], [*self.rows[1][:5], True, 0]])):
            with self.assertRaisesRegex(ProviderError, "^DEGRADED$"):
                self.read(lambda *_: body)

    def test_status_sanitization_and_no_transport_without_local_prerequisites(self):
        for failure, expected in [(HTTPError("", code, self.token, {}, None), status)
                                  for code, status in ((302, "DEGRADED"), (401, "AUTH_REQUIRED"),
                                                       (403, "AUTH_REQUIRED"), (429, "RATE_LIMITED"),
                                                       (503, "DISCONNECTED"))] + [(URLError(self.token), "DISCONNECTED")]:
            def fail(*_):
                raise failure

            with self.assertRaisesRegex(ProviderError, f"^{expected}$"):
                self.read(fail)
        for changes, code in (({"token": "bad\ntoken"}, "LOCAL_CREDENTIALS_REQUIRED"),
                              ({"key": "../orders"}, "DEGRADED"),
                              ({"interval": "30m"}, "DEGRADED"),
                              ({"reserve": lambda _op: False}, "RATE_LIMITED")):
            with self.assertRaisesRegex(ProviderError, f"^{code}$"):
                self.read(lambda *_: self.fail("transport must remain idle"), **changes)

    def test_historical_permission_ceiling(self):
        grants = {"upstox": {permission: True for permission in providers.PERMISSIONS}}
        self.assertEqual(providers.route(["upstox"], "historical", providers.PURPOSES["import"], grants), "upstox")
        for purpose in ("historical_replay", "optimization", "automatic_sync", "export"):
            self.assertIsNone(providers.route(["upstox"], "historical", providers.PURPOSES[purpose], grants))

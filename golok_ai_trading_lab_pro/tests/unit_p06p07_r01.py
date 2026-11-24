import json
import unittest
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from urllib.error import HTTPError, URLError

from scripts.reproduce_p05 import fixture
from services import calendar, indicators, ingestion, level_research, portfolio, providers, simulation, targets, upstox
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


class LevelsTest(unittest.TestCase):
    def setUp(self):
        assets, day, self.costs = fixture()
        original = assets[0].sessions[day]
        self.session = replace(original, entry_cutoff=original.opening + timedelta(hours=2),
                               exit_cutoff=original.opening + timedelta(hours=3))
        template = assets[0].bars[0]
        self.history = [
            replace(template, open_time=original.opening + timedelta(minutes=5 * i),
                    close_time=original.opening + timedelta(minutes=5 * (i + 1)),
                    available_at=original.opening + timedelta(minutes=5 * (i + 1)),
                    open=Decimal("100"), close=Decimal("100"), high=Decimal("104"), low=Decimal("99.5"), volume=40000)
            for i in range(18)
        ]
        self.as_of = self.history[-1].available_at + timedelta(seconds=1)
        self.expiry = self.as_of + timedelta(minutes=2)

    def evaluate(self, history, as_of=None):
        return level_research.evaluate(history, self.session, as_of or self.as_of, self.expiry,
                                       Decimal("99.50"), Decimal(".05"), "NSE", self.costs, simulation.RiskPolicy())

    def test_entry_stop_and_future_data_invariance(self):
        report = self.evaluate(self.history)
        self.assertEqual(report["status"], "RESEARCH_PROPOSAL")
        self.assertEqual(report["range"], (Decimal("99.50"), Decimal("101")))
        self.assertEqual(report["selected"]["limit"], Decimal("100"))
        self.assertEqual(report["selected"]["stop"], Decimal("99.50"))
        future = replace(self.history[-1], available_at=self.as_of, low=Decimal("1"), high=Decimal("1000"))
        self.assertEqual(self.evaluate(self.history + [future]), report)
        opening = self.as_of + timedelta(seconds=1)
        self.assertTrue(level_research.eligible_open(report, opening, Decimal("100")))
        self.assertFalse(level_research.eligible_open(report, opening, Decimal("100.05")))
        self.assertFalse(level_research.eligible_open(report, self.expiry, Decimal("100")))
        self.assertEqual(self.evaluate(self.history, self.expiry)["status"], "NO_TRADE")

    def test_atr_target_caps_without_bypassing_barrier_and_independent_values(self):
        last = replace(self.history[-1], high=Decimal("101"))
        history = self.history[:-1] + [last]
        values = indicators.calculate(self.history)
        self.assertEqual(values["atr14"][-1], Decimal("4.5"))
        self.assertEqual(values["rsi14"][-1], Decimal("50"))
        self.assertEqual(values["ema20"][-1], None)
        entry, stop = Decimal("100"), Decimal("99.50")
        results = [targets.levels(history, entry, stop, policy, self.as_of, self.session.exit_cutoff)[0]
                   for policy in ("structure", "fixed_4r", "atr_barrier")]
        self.assertEqual(results, [(Decimal("101"),), (Decimal("102.00"),), (Decimal("101"),)])
        high_resistance = [replace(bar, high=Decimal("110"), low=Decimal("99.5")) for bar in self.history[:1]]
        high_resistance += [replace(bar, open=Decimal("99"), close=Decimal("99"),
                                    high=Decimal("100"), low=Decimal("98.5")) for bar in self.history[1:]]
        self.assertLess(targets.levels(high_resistance, entry, stop, "atr_barrier", self.as_of,
                                       self.session.exit_cutoff)[0][0], Decimal("110"))

    def test_portfolio_freezes_joint_levels_and_checks_next_open(self):
        session = replace(self.session, entry_cutoff=self.session.opening + timedelta(minutes=105),
                          exit_cutoff=self.session.opening + timedelta(minutes=110),
                          closing=self.session.opening + timedelta(minutes=110))
        prices = Decimal
        history = [
            replace(self.history[0], open_time=start, close_time=end, available_at=end,
                    open=prices("100"), high=prices("100.20"), low=prices("99.95"),
                    close=prices("100"), volume=10000)
            for start, end in session.slots(300)
        ]
        history[2] = replace(history[2], high=prices("115"))
        history[16] = replace(history[16], high=prices("101"), close=prices("101"), volume=40000)
        history[17] = replace(history[17], open=prices("101"), high=prices("101.1"), close=prices("101"))
        history[18] = replace(history[18], open=prices("100.20"), high=prices("101.30"), close=prices("101"))
        asset = portfolio.Series("FIXTURE", "NSE", prices(".05"), tuple(history), {session.day: session})

        def experiment(series):
            return portfolio.replay((series,), session.day, session.day, 300, ("ST-06",), self.costs,
                                    target_policy=targets.JOINT_POLICY)

        filled = experiment(asset)
        first = filled["decisions"][0]
        self.assertEqual(first["level_proposal"]["status"], "RESEARCH_PROPOSAL")
        self.assertTrue(first["gates"]["G06"]["passed"])
        self.assertEqual(filled["trades"][0]["stop"], first["level_proposal"]["selected"]["stop"])
        altered = list(history)
        altered[18] = replace(altered[18], open=prices("101.25"))
        missed = experiment(replace(asset, bars=tuple(altered)))
        self.assertEqual(missed["decisions"][0]["level_proposal"], first["level_proposal"])
        self.assertFalse(missed["decisions"][0]["gates"]["G06"]["passed"])

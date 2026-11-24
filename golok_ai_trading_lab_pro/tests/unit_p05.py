import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from scripts.reproduce_p05 import fixture, run
from services import decision, eligibility, market_data, portfolio, research_v3, session_policy, strategies, temporal


class P05Tests(unittest.TestCase):
    def test_every_gate_vetoes_and_unrecognized_modes_fail(self):
        checks = dict.fromkeys(decision.GATES, True)
        self.assertEqual(decision.evaluate(checks, mode="synthetic_replay")["state"], "SIMULATION_CANDIDATE")
        for gate in checks:
            with self.subTest(gate=gate):
                output = decision.evaluate({**checks, gate: 1}, mode="synthetic_replay")
                self.assertEqual(output["state"], "NO_TRADE")
                self.assertFalse(output["gates"][gate]["passed"])
        self.assertEqual(decision.evaluate(checks, mode="authorized_research")["state"], "NO_TRADE")

    def test_eligibility_is_fail_closed(self):
        self.assertEqual(eligibility.evaluate("provider", "synthetic_replay"),
                         ("HISTORICAL_AVAILABILITY_MODELED", False))
        self.assertFalse(eligibility.evaluate("provider", "authorized_research", as_of_verified="yes",
                                              authorization_verified=True)[1])
        self.assertFalse(eligibility.evaluate("synthetic", "synthetic_replay", quarantined=True)[1])
        self.assertFalse(eligibility.evaluate("unknown", "descriptive")[1])

    def test_fixture_reconciles_and_risk_rejects_a_third_instrument(self):
        result = run()["calculation"]
        self.assertEqual(len(result["decisions"]), 3)
        self.assertEqual(len(result["trades"]), 2)
        self.assertTrue(result["suspended"])
        self.assertEqual({row["reason"] for row in result["trades"]}, {"STOP_FIRST"})
        # Two 20-share trades lose 3.00 per share and pay 2.02 per round trip.
        self.assertEqual(result["ending_cash"], Decimal("50000") - 2 * (20 * Decimal("3") + Decimal("2.02")))

    def test_incomplete_late_and_quarantined_data_reject(self):
        series, day, costs = fixture()
        asset, = series[:1]
        late = replace(asset.bars[0], available_at=asset.bars[0].available_at + timedelta(seconds=1))
        for invalid in (replace(asset, bars=asset.bars[1:]), replace(asset, bars=(late, *asset.bars[1:])),
                        replace(asset, quarantined=True), replace(asset, origin="provider")):
            with self.assertRaises(ValueError):
                portfolio.replay([invalid], day, day, 300, ("ST-01",), costs)

    def test_vwap_and_reversion_use_distinct_prior_observations(self):
        day = date(2024, 1, 2)

        def bar(index, opening, high, low, closing):
            return market_data.Candle(datetime(2024, 1, 2, tzinfo=timezone.utc) + timedelta(minutes=index),
                                      *map(Decimal, (opening, high, low, closing)), 100)

        rising = [bar(index, 100 + index, 101 + index, 99 + index, 100 + index) for index in range(5)]
        self.assertEqual(strategies.vwap_reclaim_pullback([*rising, bar(5, 101, 105, 101, 104)], day),
                         Decimal("101"))
        sideways = [bar(index, 100, 102, 98, 100) for index in range(6)]
        self.assertEqual(strategies.range_reversion([*sideways, bar(6, 97, 101, 96, 99)], day), Decimal("96"))
        self.assertIsNone(strategies.vwap_reclaim_pullback(sideways, day))
        self.assertIsNone(strategies.range_reversion([*rising, rising[-1], bar(6, 97, 101, 96, 99)], day))

    def test_research_preceding_levels_and_turnover(self):
        series, _, _ = fixture()
        example = list(series[0].bars[:3]) * 7
        base = example[-1]
        breakout = replace(base, high=Decimal(110), close=Decimal(109))
        reversal = replace(base, close=Decimal(100))
        self.assertEqual(research_v3.analyze([*example, breakout])["RE-07"]["finding"]["direction"], "up")
        findings = research_v3.analyze([*example, breakout, reversal])
        self.assertTrue(findings["RE-08"]["finding"]["failed_up"])
        self.assertEqual(findings["RE-09"]["finding"]["scope"], "instrument_only")
        self.assertEqual(findings["RE-17"]["finding"]["median_close_times_volume"], "100000")
        self.assertIsNone(research_v3.analyze(example, True)["RE-17"]["finding"])

    def test_walk_forward_excludes_holdout_and_embargo(self):
        days = tuple(date(2024, 1, 1) + timedelta(days=index) for index in range(18))
        frozen = temporal.freeze(days[:4], days[5:12], days[13:], embargo=1)
        windows = temporal.walk_forward(frozen, train_size=3, validation_size=2)
        self.assertEqual(len(windows), 3)
        for train, validate in windows:
            self.assertGreater(validate[0] - train[-1], timedelta(days=1))
            self.assertTrue(set(train + validate).isdisjoint(frozen.holdout))
        with self.assertRaises(FrozenInstanceError):
            frozen.embargo = 0
        with self.assertRaises(ValueError):
            temporal.freeze(days[:5], days[5:12], days[13:], embargo=1)

    def test_session_deadline_and_expired_authorization(self):
        now = datetime.fromisoformat("2024-01-02T23:59:50+05:30")
        self.assertEqual(session_policy.deadline(now) - now, timedelta(seconds=10))
        self.assertEqual(session_policy.deadline(now - timedelta(hours=1)) - (now - timedelta(hours=1)),
                         timedelta(minutes=30))
        for offset, expected in ((-1, False), (0, True), (25, True), (26, False)):
            self.assertIs(session_policy.fresh("000000", (now - timedelta(seconds=offset)).isoformat(), now), expected)
        self.assertFalse(session_policy.fresh("000000", "2024-01-02T23:59:50", now))

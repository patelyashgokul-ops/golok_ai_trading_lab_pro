import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from scripts.reproduce_p05 import fixture
from services import decision, portfolio, replay_contract, rights_lifecycle, session_clock


class P08Tests(unittest.TestCase):
    def test_storage_disposition_is_bounded_by_declared_rights(self):
        day = datetime(2024, 1, 2).date()
        self.assertEqual(rights_lifecycle.state(day, day, day, False, "fixed"), "active")
        self.assertEqual(rights_lifecycle.state(day, day, None, False, "fixed"), "insufficient")
        self.assertEqual(rights_lifecycle.state(day, day, day - timedelta(days=1), False, "fixed"),
                         "retention_expired")
        self.assertEqual(rights_lifecycle.state(day, day, day, True, "archive"), "revoked")
        self.assertFalse(rights_lifecycle.can_persist("active", "transient"))

    def test_calendar_phase_uses_explicit_windows(self):
        data, day, _ = fixture()
        session = data[0].sessions[day]
        self.assertEqual(session_clock.phase(session, session.opening - timedelta(seconds=1)), "pre_market")
        self.assertEqual(session_clock.phase(session, session.opening), "market_opening")
        self.assertEqual(session_clock.phase(session, session.opening + timedelta(minutes=5)), "intraday")
        self.assertEqual(session_clock.phase(session, session.closing), "post_market")
        self.assertEqual(session_clock.phase(replace(session, kind="closed"), session.opening), "closed")
        self.assertEqual(session_clock.phase(None, session.opening), "blocked")
        end = session.opening + timedelta(minutes=5)
        split = replace(session, segments=((session.opening, end), (end + timedelta(minutes=10), session.closing)))
        self.assertEqual(session_clock.phase(split, end), "maintenance")

    def test_historical_intake_requires_affirmative_evidence_and_prior_publication(self):
        p = replay_contract.Provenance("historical_intraday", "5m", "a" * 64, "verified_publication",
                                        True, True, True, True)
        close = datetime(2024, 1, 2, 4, 0, tzinfo=timezone.utc)
        receipt = close + timedelta(seconds=2)
        now = receipt + timedelta(seconds=1)

        def assess(provenance, decision_at=now):
            return replay_contract.publication_evidence(provenance, close=close, published=receipt,
                                                         decision_at=decision_at)

        self.assertEqual(assess(p), "HISTORICAL_INTAKE_ONLY")
        self.assertEqual(assess(p, receipt), "UNAVAILABLE_AT_DECISION")
        self.assertEqual(assess(replace(p, permission=1)), "MISSING_PERMITTED_EVIDENCE")
        self.assertEqual(assess(replace(p, publication_basis="first_observed_receipt")), "UNSUPPORTED_MODE_OR_PUBLICATION")
        self.assertEqual(assess(replace(p, mode="live")), "UNSUPPORTED_MODE_OR_PUBLICATION")
        self.assertEqual(assess(replace(p, mode="historical_daily", interval="1d",
                                        publication_basis="first_observed_receipt")), "DESCRIPTIVE_ONLY")

    def test_intraday_contract_never_executes_at_or_before_publication(self):
        data, day, costs = fixture()
        base = data[0]
        bars = list(base.bars)
        bars[3] = replace(bars[3], available_at=bars[4].open_time + timedelta(seconds=1))
        asset = replace(base, origin="historical_contract", bars=tuple(bars))
        proof = replay_contract.Provenance("historical_intraday", "5m", replay_contract.fingerprint(asset),
                                           "verified_publication", True, True, True, True)
        result = replay_contract.replay_fixture([asset], {asset.key: proof}, day, day, 300,
                                                ("ST-01",), costs, target_policy="fixed_4r")
        self.assertEqual(len(result["trades"]), 1)
        self.assertGreater(result["trades"][0]["time"], bars[3].available_at)
        self.assertEqual(result["scope"], "HISTORICAL_CONTRACT_FIXTURE_ONLY")
        self.assertEqual(result["decisions"][0]["live_actionability"], "BLOCKED")
        for invalid in (replace(proof, permission=False), replace(proof, fingerprint="0" * 64),
                        replace(proof, publication_basis="first_observed_receipt")):
            with self.assertRaisesRegex(ValueError, "provenance"):
                replay_contract.replay_fixture([asset], {asset.key: invalid}, day, day, 300, ("ST-01",), costs)
        with self.assertRaisesRegex(ValueError, "Synthetic portfolio source"):
            portfolio.replay([asset], day, day, 300, ("ST-01",), costs)

    def test_gate_context_cannot_override_a_veto(self):
        checks = dict.fromkeys(decision.GATES, True)
        checks["G01"] = ("unverified", "verified", "yes")
        blocked = decision.evaluate(checks, mode="synthetic_replay",
                                    context={"passed": True, "status": "PASSED", "mode": "live"})
        self.assertEqual(blocked["state"], "NO_TRADE")
        self.assertFalse(blocked["gates"]["G01"]["passed"])
        self.assertEqual(blocked["gates"]["G01"]["status"], "FAILED")
        self.assertEqual(blocked["gates"]["G01"]["mode"], "synthetic_replay")

import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from scripts.reproduce_p05 import fixture
from services import replay_contract, session_clock


class P08Tests(unittest.TestCase):
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

"""Validate typed time and permission evidence before a historical research mode."""

import re
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from hashlib import sha256

from . import backtest, portfolio, simulation


@dataclass(frozen=True)
class Provenance:
    mode: str
    interval: str
    fingerprint: str
    publication_basis: str
    permission: bool
    instrument_verified: bool
    calendar_verified: bool
    quality_verified: bool


def publication_evidence(provenance, *, close, published, decision_at):
    """An intake assessment can never grant live or financial approval."""
    if not isinstance(provenance, Provenance) or not re.fullmatch(r"[a-f0-9]{64}", provenance.fingerprint):
        return "INVALID_PROVENANCE"
    if any(not isinstance(value, datetime) or value.utcoffset() is None for value in (close, published, decision_at)):
        return "MISSING_TIMESTAMPS"
    if not close <= published < decision_at:
        return "UNAVAILABLE_AT_DECISION"
    if not all(value is True for value in (provenance.permission, provenance.instrument_verified,
                                            provenance.calendar_verified, provenance.quality_verified)):
        return "MISSING_PERMITTED_EVIDENCE"
    if provenance.mode == "historical_daily" and provenance.interval == "1d" and provenance.publication_basis in (
            "verified_publication", "first_observed_receipt"):
        return "DESCRIPTIVE_ONLY"
    if provenance.mode == "historical_intraday" and provenance.interval in ("1m", "3m", "5m", "15m"):
        if provenance.publication_basis == "verified_publication":
            return "HISTORICAL_INTAKE_ONLY"
    return "UNSUPPORTED_MODE_OR_PUBLICATION"


def fingerprint(asset):
    sessions = {day.isoformat(): asdict(session) for day, session in asset.sessions.items()}
    return sha256(backtest.canonical({
        "asset": asset.key, "exchange": asset.exchange, "tick": asset.tick,
        "sessions": sessions, "bars": [asdict(bar) for bar in asset.bars],
    }).encode()).hexdigest()


def replay_fixture(series, provenance, starts, ends, seconds, codes, costs, *, target_policy="structure",
                   capital=Decimal("50000")):
    """Exercise historical timing on authored fixtures without enabling a market-data ORM route."""
    return replay_historical(series, provenance, starts, ends, seconds, codes, costs, target_policy=target_policy,
                             capital=capital, fixture=True)


def replay_historical(series, provenance, starts, ends, seconds, codes, costs, *, target_policy="structure",
                      capital=Decimal("50000"), fixture=False):
    intervals = {60: "1m", 180: "3m", 300: "5m", 900: "15m"}
    if not isinstance(costs, simulation.CostSchedule) or seconds not in intervals:
        raise ValueError("The test contract requires supported intraday intervals and explicit costs.")
    for asset in series:
        proof = provenance.get(asset.key)
        if (not isinstance(proof, Provenance) or proof.mode != "historical_intraday"
                or proof.interval != intervals[seconds] or proof.fingerprint != fingerprint(asset)
                or proof.publication_basis != "verified_publication"
                or not all(value is True for value in (proof.permission, proof.instrument_verified,
                                                        proof.calendar_verified, proof.quality_verified))):
            raise ValueError("Historical fixture provenance is missing, mismatched or unauthorized.")
        publications = [bar.available_at for bar in asset.bars]
        if any(not isinstance(at, datetime) or at.utcoffset() is None for at in publications):
            raise ValueError("Every fixture requires an explicit publication timestamp.")
        if any(left > right for left, right in zip(publications, publications[1:])):
            raise ValueError("Out-of-order publication is unsupported by this replay contract.")
    return portfolio._replay(series, starts, ends, seconds, codes, costs, capital=capital,
                             portfolio_policy=portfolio.PortfolioPolicy(), target_policy=target_policy,
                             historical="fixture" if fixture else "authorized")

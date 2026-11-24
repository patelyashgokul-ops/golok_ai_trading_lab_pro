"""Validate typed time and permission evidence before a historical research mode."""

import re
from dataclasses import dataclass
from datetime import datetime


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

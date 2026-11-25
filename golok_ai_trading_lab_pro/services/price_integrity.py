"""Compare equivalent closing observations without treating shared feeds as independent."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Observation:
    isin: str
    venue: str
    currency: str
    interval: str
    adjustment: str
    close_at: datetime
    received_at: datetime
    price: Decimal
    upstream: str


def compare(left, right, as_of, tolerance):
    if (as_of.utcoffset() is None or not isinstance(tolerance, Decimal) or not tolerance.is_finite()
            or tolerance < 0):
        raise ValueError("Require an explicit cutoff and nonnegative absolute price tolerance.")
    dimensions = ("isin", "venue", "currency", "interval", "adjustment", "close_at")
    for observation in (left, right):
        if (any(not getattr(observation, key) for key in dimensions)
                or observation.close_at.utcoffset() is None or observation.received_at.utcoffset() is None
                or not observation.close_at <= observation.received_at <= as_of
                or not isinstance(observation.price, Decimal) or not observation.price.is_finite()
                or observation.price <= 0):
            return "UNVERIFIABLE"
    if any(getattr(left, key) != getattr(right, key) for key in dimensions):
        return "NON_EQUIVALENT"
    if abs(left.price - right.price) > tolerance:
        return "CONFLICT"
    upstreams = tuple(value.strip().casefold() if isinstance(value, str) else "" for value in (left.upstream, right.upstream))
    if any(value in ("", "unknown") for value in upstreams):
        return "UNKNOWN_LINEAGE"
    return "SHARED_UPSTREAM" if upstreams[0] == upstreams[1] else "MATCH"


def compare_bars(left, right, left_bar, right_bar, as_of, tolerance):
    validity = compare(left, right, as_of, tolerance)
    if validity in ("UNVERIFIABLE", "NON_EQUIVALENT"):
        return validity, {}
    differences = {name: abs(getattr(left_bar, name) - getattr(right_bar, name))
                   for name in ("open", "high", "low", "close", "volume")}
    if differences["volume"] or any(differences[key] > tolerance for key in ("open", "high", "low", "close")):
        return "CONFLICT", differences
    return validity, differences

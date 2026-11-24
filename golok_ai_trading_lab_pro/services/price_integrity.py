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
    if not left.upstream or not right.upstream or "unknown" in (left.upstream, right.upstream):
        return "UNKNOWN_LINEAGE"
    return "SHARED_UPSTREAM" if left.upstream == right.upstream else "MATCH"

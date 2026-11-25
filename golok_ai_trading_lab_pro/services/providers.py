"""Capability ceilings for read-only sources. Entitlement is a separate input."""

from dataclasses import dataclass

CONTRACT_VERSION = "provider-capabilities-1"

@dataclass(frozen=True)
class Source:
    name: str
    feed: str
    permissions: frozenset
    upstream: str


@dataclass(frozen=True)
class Capability:
    documented: bool
    implemented: bool
    configured: bool | None
    authorized: bool | None
    connectivity_verified: bool | None
    quality_verified: bool | None
    eligible: bool


PERMISSIONS = frozenset({"query", "display", "persist", "automatic", "backtest", "optimize",
                         "fit", "live", "export", "research"})
PURPOSES = {
    "query": ("query",),
    "display": ("display",),
    "import": ("query", "display", "persist"),
    "persist": ("persist",),
    "research": ("display", "research"),
    "historical_replay": ("display", "backtest"),
    "optimization": ("display", "backtest", "optimize"),
    "fitting": ("display", "fit"),
    "automatic_sync": ("query", "display", "persist", "automatic"),
    "prospective_paper": None,
    "live": None,
    "export": ("display", "export"),
    "redistribution": None,
}
SOURCES = {
    "fixture": Source("Synthetic fixture", "synthetic", PERMISSIONS - {"live"}, "fixture"),
    "bhavcopy": Source("NSE Bhavcopy local file", "daily", frozenset({"query", "display", "persist", "research"}), "NSE"),
    "manual": Source("Authorized local CSV", "historical",
                     frozenset({"query", "display", "persist", "research", "backtest"}), "declared"),
    "nse_mcp": Source("NSE official MCP", "informational", frozenset(), "NSE"),
    "yahoo": Source("Yahoo Finance", "unverified", frozenset(), "unknown"),
    "smartapi": Source("Angel One historical", "historical", frozenset({"query", "display", "persist", "research"}), "exchange"),
    "upstox": Source("Upstox historical", "historical", frozenset({"query", "display", "persist", "research"}), "NSE"),
}


def capability(*, documented, implemented, configured=None, authorized=None,
               connectivity_verified=None, quality_verified=None):
    """Current operational eligibility needs affirmative evidence at every stage."""
    required = (documented, implemented, configured, authorized, connectivity_verified, quality_verified)
    return Capability(*required, all(value is True for value in required))


def route(candidates, feed, required, grants):
    required = frozenset(required)
    if not required or not required <= PERMISSIONS:
        return None
    for key in candidates:
        source = SOURCES.get(key)
        if source and source.feed == feed and required <= source.permissions and all(
                grants.get(key, {}).get(permission) is True for permission in required):
            return key
    return None

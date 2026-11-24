"""Capability ceilings for read-only sources. Entitlement is a separate input."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    feed: str
    permissions: frozenset
    upstream: str


PERMISSIONS = frozenset({"query", "display", "persist", "automatic", "backtest", "optimize",
                         "fit", "live", "export", "research"})
SOURCES = {
    "fixture": Source("Synthetic fixture", "synthetic", PERMISSIONS - {"live"}, "fixture"),
    "bhavcopy": Source("NSE Bhavcopy local file", "daily", frozenset({"query", "display", "persist", "research"}), "NSE"),
    "manual": Source("Authorized local CSV", "historical", frozenset({"query", "display", "persist", "research"}), "declared"),
    "nse_mcp": Source("NSE official MCP", "informational", frozenset(), "NSE"),
    "yahoo": Source("Yahoo Finance", "unverified", frozenset(), "unknown"),
    "smartapi": Source("Angel One historical", "historical", frozenset({"query", "display", "persist", "research"}), "exchange"),
    "upstox": Source("Upstox", "unverified", frozenset(), "exchange"),
}


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

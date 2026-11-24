"""Effective-dated mapping for explicitly supplied equity reference records."""

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from . import upstox


@dataclass(frozen=True)
class Mapping:
    instrument_key: str
    exchange: str
    symbol: str
    provider: str
    token: str
    starts: date
    ends: date | None
    tick: Decimal
    lot: int
    status: str
    source: str
    version: str
    verification: str
    isin: str | None = None
    sector: str | None = None

    def __post_init__(self):
        if (not all(isinstance(value, str) and value.strip()
                    for value in (self.instrument_key, self.symbol, self.provider, self.source, self.version))
                or self.exchange not in ("NSE", "BSE")
                or (not upstox.identity(self.exchange, self.token, self.isin) if self.provider == "upstox"
                    else not isinstance(self.token, str) or not re.fullmatch(r"[0-9]{1,20}", self.token))
                or self.status not in ("listed", "suspended", "delisted")
                or self.verification not in ("reviewed", "unverified", "fixture")
                or type(self.starts) is not date or (self.ends is not None and (type(self.ends) is not date or self.ends <= self.starts))
                or not isinstance(self.tick, Decimal) or not self.tick.is_finite() or self.tick <= 0
                or type(self.lot) is not int or self.lot <= 0
                or (self.isin is not None and not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", self.isin))):
            raise ValueError("Invalid equity reference record.")


class MappingBook:
    def __init__(self, records):
        if len(records) > 10000:
            raise ValueError("Reference mappings exceed the supported batch size.")
        self._tokens = defaultdict(list)
        symbols = defaultdict(list)
        instruments = defaultdict(list)
        for mapping in records:
            prefix = (mapping.provider, mapping.exchange)
            self._tokens[(*prefix, mapping.token)].append(mapping)
            symbols[(*prefix, mapping.symbol.casefold())].append(mapping)
            instruments[(*prefix, mapping.instrument_key)].append(mapping)
        for groups in (self._tokens, symbols, instruments):
            for group in groups.values():
                group.sort(key=lambda row: row.starts)
                if any(a.ends is None or a.ends > b.starts for a, b in zip(group, group[1:])):
                    raise ValueError("Overlapping token, symbol or instrument validity.")

    def resolve(self, provider, exchange, token, day, *, synthetic=False):
        eligible_verification = "fixture" if synthetic else "reviewed"
        for row in self._tokens.get((provider, exchange, token), ()):
            if row.starts <= day and (row.ends is None or day < row.ends):
                if row.status == "listed" and row.verification == eligible_verification:
                    return row
                break
        raise ValueError("No eligible instrument mapping for the requested date.")

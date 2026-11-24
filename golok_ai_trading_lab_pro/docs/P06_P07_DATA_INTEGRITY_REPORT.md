# P06–P07 data integrity

Upstox accepts one completed NSE cash-equity session and a reviewed NSE_EQ key bound to an effective ISIN mapping and calendar. The V3 response must contain the exact session-grid count. JSON size, price precision, OHLC relationships, integral volume and receipt timestamps are validated. The response is sorted before normalization. A missing interval, repeated timestamp or wrong session fails the complete import. Provider publication is unknown and receipt establishes local availability.

Historical sync serializes work per instrument using the existing replay guard. The automatic check examines at most eight other eligible datasets for the same instrument, ISIN, interval and provenance class from a different supported broker. It checks common closed candles, including opening time and matching raw OHLCV scope. Price difference above the larger mapped tick or any volume mismatch sets both datasets' integrity conflict flags and saves the comparison audits. Research and replay paths recheck the veto. Independent source confirmation requires distinct documented upstreams. The fixture case uses unknown lineage.

Broker comparisons with reviewed identical venue lineage are classified as shared upstream. Adjustment metadata participates in equivalence, and an unknown raw-share basis restricts a provider comparison. Full corporate-action-aware reconciliation and automatic comparison for arbitrary imports remain open. Comparison audits remain limited to the imported overlapping session. Existing one-off comparison stays available.

Fixture chronology and expiry reran. Authenticated polling, real publication latency, live-source freshness and complete stale-feed recovery remain unverified. No market data was acquired.

[Fixture, authorization, concurrency and coverage evidence](evidence/p06_p07_repair/INDEX.md)

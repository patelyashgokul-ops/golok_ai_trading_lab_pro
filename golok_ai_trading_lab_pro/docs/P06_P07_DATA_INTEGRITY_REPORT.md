# P06–P07 data integrity

Upstox accepts one completed NSE cash-equity session and a reviewed NSE_EQ key bound to an effective ISIN mapping and calendar. The V3 response must contain the exact session-grid count. JSON size, price precision, OHLC relationships, integral volume and receipt timestamps are validated. The response is sorted before normalization. A missing interval, repeated timestamp or wrong session fails the complete import. Provider publication is unknown and receipt establishes local availability.

Historical sync serializes work per instrument using the existing replay guard. The automatic check examines at most eight other eligible datasets for the same instrument, ISIN, interval and provenance class from a different supported broker. It checks common closed candles, including opening time and matching raw OHLCV scope. Price difference above the larger mapped tick or any volume mismatch sets both datasets' integrity conflict flags and saves the comparison audits. Research and replay paths recheck the veto. Independent source confirmation requires distinct documented upstreams. The fixture case uses unknown lineage.

Broker comparisons with reviewed identical venue lineage are classified as shared upstream. Adjustment metadata participates in equivalence, and an unknown raw-share basis restricts a provider comparison. Full corporate-action-aware reconciliation and automatic comparison for arbitrary imports remain open. Comparison audits remain limited to the imported overlapping session. Existing one-off comparison stays available.

Fixture chronology and expiry reran. Authenticated polling, real publication latency, live-source freshness and complete stale-feed recovery remain unverified. No market data was acquired.

The follow-up verifies the operator-run history queue using the same source comparison and veto path. An independent wrong-data suite covers conflicting instrument key and venue, future candle, negative price, adjusted/raw and currency boundaries, scaled price conflict, stale receipt and expired authorization.

## Release 20.0.9.1.4

Mapped intake and verified manual comparison snapshots share one automatic comparison service. Eligible observations include reviewed broker history, authorized raw Bhavcopy daily observations and an administrator-verified local CSV. Analyst uploads require independent evidence and a frozen complete dataset before they can affect another source's eligibility. The attestation records the reviewer and dataset fingerprint. Historical publication approval and backtesting rights use their own controls.

Both sources require matching instrument, ISIN, interval, calendar session windows and candle open/close edges. Each source requires active descriptive research permission. A raw-share declaration is required for authorized market data. A nearby published split or bonus ratio can explain a material disagreement and is logged as a possible adjustment mismatch. It still blocks research from both affected sources. Observations from the same exchange upstream do not count as independent confirmation.

An administrator can record a distinct replacement for an existing conflict after a current independent source matches the same observation. The correction reference, reviewer, timestamp, original audit, original candles and original conflict flags are retained. The application keeps both original datasets blocked. A dataset replacement is evidence for research access and does not authorize financial or executable use.

[Fixture, authorization, concurrency and coverage evidence](evidence/p06_p07_repair/INDEX.md)

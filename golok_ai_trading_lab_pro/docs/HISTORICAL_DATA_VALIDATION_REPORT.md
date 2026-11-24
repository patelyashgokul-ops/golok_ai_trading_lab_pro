# Historical data validation — P06

P08 normalizes accepted legacy and targeted UDiFF audits into the same research dataset with a matching NSE mapping, exact ISIN and conservative local receipt. Odoo tests detected and backfilled a missing daily session. The workflow used project-authored fixtures. Authorized genuine acquisition remains blocked. [P08 authorization and datasets](P08_AUTHORIZATION_AND_DATASET_REPORT.md)

P07 acquired zero authorized market sessions. The reader now validates a bounded modern NSE cash UDiFF profile for date, venue, identity, series and OHLCV. The tests used authored CSV rows. Official exchange-file comparison and integration into the candle research panel remain open. [P07 provider review](FREE_MARKET_DATA_PROVIDER_EVALUATION.md)

**Authorized external acquisition recorded zero market sessions.** The review established public documentation and report listings. It did not establish the required permission to automate retrieval, retain market panels and optimize strategies. The archive contains synthetic OHLCV only.

The local reader recognizes the legacy NSE cash-market CSV header and its optional empty trailing column. It validates UTF-8, EQ series, trading date, symbol, ISIN syntax, positive OHLC consistency and bounded integer volume. It accepts a bounded single-member CSV ZIP, rejects unsafe member names and oversized expansions, and requires an explicit completed session on an NSE calendar with matching provenance. No timestamp inside the daily record is treated as an intraday publication time.

Accepted daily rows, original file SHA-256, calendar, authorization reference and receipt audit remain in the company database. Invalid imports retain a quarantine decision and digest without storing their raw bytes. A conflicting accepted session is blocked. Exact repeats return the existing record. The comparison service checks venue, ISIN, currency, interval, adjustment, close, receipt and upstream identity. Automated cross-provider comparison, verification against an authorized official UDiFF file and downstream replay of authorized daily batches remain open. [Unit cases](../tests/unit_p06.py) · [Odoo cases](../tests/test_lab.py)

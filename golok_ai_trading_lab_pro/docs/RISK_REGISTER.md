# Risk register

| ID | Impact | Current control | Remaining work |
|---|---|---|---|
| R-01 | Action on synthetic or stale market data | Historical decision constrained to NO TRADE | Validate calendar, quote age and market provenance before enabling eligibility |
| R-02 | Misidentified symbols or unusable historical observations | Immutable manual instrument and dataset identifiers, format and OHLC checks | Map official tokens and corporate actions, verify calendars and candle completeness |
| R-03 | Competing ingest transactions | Database unique key, atomic request and repeatable import | Independent-transaction tests and controlled retry for racing requests |
| R-04 | Cross-company disclosure | Odoo 20 role grants, global company filters and dataset authorization | Expand tests to each new integration and user-facing path |
| R-05 | Overstated evidence from limited historical data | Versioned cutoff snapshots, sufficient sample checks, no actionable output | Point-in-time data, cost model, leakage tests, calibrated and prospective results |
| R-06 | Broker credentials or entitlement misuse | Initial app has no credential or broker endpoint fields | Confirm account terms and static egress requirements, add redaction and tests |
| R-07 | Resource saturation or failed workstation jobs | 4,000-row import limit, 250-bar research limit, manual refresh | Performance profiles, retention, queue, recovery and workload budgets |
| R-08 | Misleading accounting or unintended transaction | No paper or real order path | Implement paper ledger and reconcile virtual balances before paper readiness |
| R-09 | Dataset correction misrepresented as original history | Immutable stored rows and hash-addressed snapshots | Add explicit revision lineage and data availability metadata |

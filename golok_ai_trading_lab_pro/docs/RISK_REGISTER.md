# Risk register

| ID | Impact | Current control | Remaining work |
|---|---|---|---|
| R-01 | Action on synthetic or stale market data | Historical decision constrained to NO TRADE | Validate calendar, quote age and market provenance before enabling eligibility |
| R-02 | Misidentified symbols or unusable historical observations | Immutable manual instrument and dataset identifiers, format and OHLC checks | Map official tokens and corporate actions, verify calendars and candle completeness |
| R-03 | Competing ingest transactions | Database unique key and replay exercised with independent PostgreSQL connections | Controlled automatic retry for racing requests |
| R-04 | Cross-company disclosure | Odoo 20 role grants, global company filters and dataset authorization | Expand tests to each new integration and user-facing path |
| R-05 | Overstated evidence from limited historical data | Versioned cutoff snapshots, sufficient sample checks, no actionable output | Point-in-time data, cost model, leakage tests, calibrated and prospective results |
| R-06 | Broker credentials or entitlement misuse | Initial app has no credential or broker endpoint fields | Confirm account terms and static egress requirements, add redaction and tests |
| R-07 | Resource saturation or failed workstation jobs | 4,000-row import limit, 250-bar research limit, manual refresh | Performance profiles, retention, queue, recovery and workload budgets |
| R-08 | Misleading accounting or unintended transaction | No paper or real order path | Implement paper ledger and reconcile virtual balances before paper readiness |
| R-09 | Dataset correction misrepresented as original history | Immutable stored rows and hash-addressed snapshots | Add explicit revision lineage and data availability metadata |
| R-10 | Vendor publication timestamp is incorrect | Strict format and cutoff checks; provenance stays operator-supplied | Independently authenticate publication and revision history |
| R-11 | Wrong provider token on a historic date | In-memory overlap and effective-date checks | Persist validated mappings and require them on ingestion |
| R-12 | Closing auction or special timetable incorrectly applied | Explicit single continuous date-specific grid | Integrate revised calendars, split sessions and instrument calendars |
| R-13 | Synthetic backtest overinterpreted | Test fixtures and CLI results identify synthetic-only provenance | Verified fee pack, approved data and preregistered holdout |
| R-14 | Virtual cash posted twice | Account row lock and unique replay batch; independent overlap test | Partial fills and prospective execution require separate reconciliation |
| R-15 | Provider credentials leak through diagnostics | Environment only, allowlisted transport, no returned session secrets | Real authorization and production controls remain unverified |

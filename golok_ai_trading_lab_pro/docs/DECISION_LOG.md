# Decision log

| ID | Decision | Consequence |
|---|---|---|
| D-001 | Start with historical CSV and manual instrument registration | The app runs without credentials. Automated master sync and SmartAPI remain future work. |
| D-002 | Store exact Decimal OHLC as text and calculate from Decimal | Round-trips avoid binary price rounding. Numeric database aggregations will need a numeric representation migration. |
| D-003 | Use explicit close timestamps and immutable provenance | Repeated identical candle imports are idempotent. Corrections require a distinct, documented dataset revision. |
| D-004 | Limit snapshot research to the latest 250 eligible bars and suppress findings on observed intraday gaps | Work is bounded per research run. ATR depends on the bounded warm-up window. |
| D-005 | Return only a historical NO TRADE decision | Live eligibility, transaction costs, strategies and monitoring can be introduced together after validation. |
| D-006 | Use the installed Odoo 20 `ir.access` API | The first install exposed a security-model change. ACLs and company rules share the native Odoo 20 CSV afterward. |
| D-007 | Use isolated disposable localhost databases and headless Edge | Verification avoids changes to owner databases. Test credentials stay out of the source and evidence. |
| D-008 | Offer manual dashboard refresh | The initial overview sends no periodic polling traffic. It has one RPC per refresh. |
| D-009 | Make calendar coverage and source publication time explicit | Unknown dates fail closed and existing legacy datasets remain readable. |
| D-010 | Keep broker REST opt-in and outside Odoo | Fixture tests can verify constraints without transmitting credentials. |
| D-011 | Prefer session-exact synthetic replay and code/input fingerprints | Reproducibility is measurable while financial validation remains blocked. |
| D-012 | Require digest match for a chart | Historical display cannot silently adopt new bars after a backfill. |
| D-013 | Preserve the P01 source as a ZIP and independently verify the populated migration | No Git repository exists in the workspace or its add-on parent. A future repository should import the checkpoint as a local baseline, excluding runtime and credential data. |
| D-014 | Use PostgreSQL range exclusions for immutable mappings | Adjacent effective intervals remain valid; concurrent overlap is rejected in the database. |
| D-015 | Post fully closed historical replay batches in whole paise | Ledger evaluation is auditable while prospective simulation stays disabled. |
| D-016 | Stop the synthetic experiment at the first unresolvable session | Preserve recorded results and avoid fabricating execution or subsequent equity. |
| D-017 | Keep manual historical research jobs bounded and transactional | A stopped worker has no external effects and the database can release its claim. |

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

# P09 prospective fixture paper accounts

The native workspace persists a separate INR 50,000 fixture-only account, one open or pending position per account, whole-paise cash and risk, and an append-only journal. A risk manager can reserve an authored test order, then process separate fixture entry and exit events. Repeating an entry or exit action for the same state has no additional effect. Tests cover cancelled reservations, closed P&L and unresolved exposure without a made-up exit.

The authored target fixture uses entry 100, stop 98 and explicit benchmark target 108. The adverse fixture models an opening gap to 97 and applies that price rather than the target. The missing-observation fixture leaves the position unresolved. Timestamps record processing, and the journal is separate from the historical replay ledger.

This is a manually advanced software fixture. It does not convert research candidates into orders or consume a general OHLC event stream. It has no partial-fill, live-feed or delayed-feed execution. [Account and journal](../models/prospective.py)

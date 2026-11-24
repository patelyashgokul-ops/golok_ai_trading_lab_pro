# P09 prospective fixture paper accounts

## P09.1 automatic fixture execution

An administrator can bind one fixture account to up to 16 research schedules, choose an existing strategy and choose the structure target or explicit 4R benchmark. The job evaluates completed, received, contiguous candles against the strategy, costs and risk limits. It persists the actual signal SHA-256 and reserves cash and risk atomically with the candidate. Schedules share one capital balance and one active exposure. The lifecycle distinguishes experimental, watch, rejection, expiry, invalidation, waiting, pending, open, closed, cancelled and unresolved outcomes. Scripted scenarios remain available on accounts without a bound schedule.

The scheduler checks later completed and received candles. Entry uses a strictly later modeled opening price, must stay inside the limit and must satisfy the 1% participation check. The first observation may stop out a new position, and its target is withheld because the event order is unknown. Later ambiguous candles use the stop first, adverse gaps use the modeled opening price, and a valid cutoff close is used for square-off. Missing coverage at session close leaves a reconciliation-required position. All timestamps distinguish the source candle and actual time the fixture was processed. This mode uses authored observations and has no broker connection.

The native workspace persists a separate INR 50,000 fixture-only account, one open or pending position per account, whole-paise cash and risk, and an append-only journal. A risk manager can reserve an authored test order, then process separate fixture entry and exit events. Repeating an entry or exit action for the same state has no additional effect. Tests cover cancelled reservations, closed P&L and unresolved exposure without a made-up exit.

The authored target fixture uses entry 100, stop 98 and explicit benchmark target 108. The adverse fixture models an opening gap to 97 and applies that price rather than the target. The missing-observation fixture leaves the position unresolved. Timestamps record processing, and the journal is separate from the historical replay ledger.

The manual scenario workflow remains available for deterministic tests. Neither fixture path supports partial fills, genuine delayed data or a verified live feed. [Account and journal](../models/prospective.py)

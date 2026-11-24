# P08 scheduler and recovery

Odoo's two-minute action reads an explicit fixture calendar in Asia/Kolkata and rotates up to 32 watches per cycle. It distinguishes pre-market, opening, intraday, post-market, closed, maintenance and missing calendar. A transaction locks each watch and persists one report per date and phase with the observation count, NO TRADE summary and optional research run. Administrators can pause the watch or check its current phase. The operations list displays persisted records.

Intraday and post-market create descriptive snapshots only from observations already available at the cutoff. Post-market counts observed earlier phases. The scheduler does not fabricate phases missed while the laptop was off. Scheduled real acquisition, restart backfill and full daily risk reporting remain open.

The existing queue uses transaction-scoped PostgreSQL SKIP LOCKED claims and now records authorization-blocked jobs. The process test holds a claim in an independent process, skips it from an Odoo worker, kills the claimant and checks for one recovered result. Durable claimed and retry leases remain open. [Phase implementation](../models/session_ops.py) · [Worker interruption harness](../scripts/verify_contention.py)

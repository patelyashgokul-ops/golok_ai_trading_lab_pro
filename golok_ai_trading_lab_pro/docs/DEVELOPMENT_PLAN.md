# Development plan

| Priority | Milestone | Dependency | Verification |
|---|---|---|---|
| 0–1 | Company-scoped historical CSV, validated storage, bounded research and overview | Odoo 20 Community and PostgreSQL | Fresh install, upgrade, Python unit, ORM and real browser checks |
| 1 | Verified exchange calendar, mapping and corporate-action data, then SmartAPI historical adapter | Account entitlement, primary documentation access and approved IP | Response fixtures, schema and recovery tests, authorized read-only API smoke test |
| 2 | Versioned opening-range research candidate and transaction-cost/risk/backtest slice | Complete calendar and provenance, verified tariff assumptions | Next-bar execution, stop-first ambiguity, holdout, costs, risk and data-leakage tests |
| 2 | Atomic virtual ledger with paper fills and session closing | Backtest execution semantics and verified data | Simultaneous transactions, duplicate delivery, interruption and reconciliation |
| 3 | Expanded OWL dashboards, persistent scheduler and health | Stable evidence and ledger schemas | KPI reconciliation, error states, timing, independent scheduler transactions |
| 4 | Broader strategy and research library | Sufficient point-in-time datasets | Walk-forward, stability, uncertainty and prospective paper evidence |

Keep research candidates inactivated until their validation and approval paths exist. Add authorized broker streaming only after a read-only adapter passes contract tests. Document the workload before publishing throughput figures.

P03 should persist effective-dated references, introduce verified source/adjustment policies, and link the REST adapter to a supervised diagnostic workflow. Follow with chronological experiment manifests, multi-session replay and independently reconciled tariffs. Add automatic virtual fills only after the ledger and portfolio invariants are independently verified.

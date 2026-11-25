# P06P07-R01 evidence

| Evidence | Artifact |
|---|---|
| P09.1 archive hash, source checkpoint and previous output parity | [Baseline](baseline.log) · [Source scan](baseline-source.log) · [Stress baseline](baseline-stress.json) |
| Original acceptance and defects | [Reconciliation](original-reconciliation.log) · [180-row matrix](../../P06_P07_COMPLETION_MATRIX.md) · [Defect closure](../../P06_P07_DEFECT_CLOSURE_REPORT.md) |
| Standalone tests, R01 fixtures and scan | [Baseline suite](baseline-unit.log) · [Final suite](standalone-final.log) · [Runtime inspection](source-check.log) · [Initial test failure](initial-level-tests.log) |
| Provider authorization, sync, automatic comparison, negative data checks and expiry | [Fresh Odoo](release/installation/fresh.log) · [Update](release/installation/upgrade.log) · [Provider performance](provider-performance.json) |
| Entry/stop, independent indicator references, policy comparison and five strategies | [Final suite](standalone-final.log) · [Policy result](target-policy-comparison.json) · [Strategy regression](five-strategy-regression.json) |
| Capital, concurrency and real process interruption | [Concurrent workers](release/security/contention.log) · [Stress comparison](stress-regression.json) |
| Browser and screenshots | [Edge checks](release/browser/edge.log) · [Desktop dashboard](release/screenshots/overview-desktop.png) · [Mobile dashboard](release/screenshots/overview-mobile.png) · [Prospective fixture journal](release/screenshots/prospective-fixture-journal.png) |
| Populated P09.1 migration, resources and 50-instrument reference workload | [Retained identifiers and records](migration/upgrade/retention.log) · [ORM measurement](migration/performance/orm.json) · [Environment](environment.log) |
| Download verification | [Complete manifest](manifest.sha256) · [Source manifest](source.sha256) |

The `final/` and `release/` logs cover the first R01 release. The `follow-up/` folder covers release 20.0.9.1.2.

| Follow-up evidence | Artifact |
|---|---|
| Unit tests, source check and prior stress parity | [Standalone](follow-up/standalone.log) · [Source scan](follow-up/source.log) · [Stress](follow-up/stress.log) |
| Historical experiment | [Four policy results](follow-up/four-policy-comparison.json) |
| Odoo, grid, queued Upstox sync and concurrency | [Fresh](follow-up/odoo-final/installation/fresh.log) · [Update](follow-up/odoo-final/installation/upgrade.log) · [Concurrency](follow-up/odoo-final/security/contention.log) |
| Focused integration rerun after the final chronology guard | [Odoo targeted tests](follow-up/odoo-focused.log) |
| Edge | [Browser log](follow-up/odoo-final/browser/edge.log) · [Upstox diagnostics screenshot](follow-up/odoo-final/screenshots/upstox-readiness.png) |
| Populated upgrades | [From P09.1](follow-up/migration-from-p091/upgrade/retention.log) · [From the prior R01 release](follow-up/migration-final/upgrade/retention.log) |

Real provider, genuine market and independent financial results are unavailable.

## Release 20.0.9.1.3

| Evidence | Artifact |
|---|---|
| Standalone suite, source and stress | [Unit tests](competition/standalone.log) · [Source scan](competition/source.log) · [Stress baseline parity](competition/stress.log) |
| Cohort, workspaces and recovery | [Fresh installation](competition/verified/installation/fresh.log) · [Update](competition/verified/installation/upgrade.log) · [Overlap and recovery](competition/verified/security/contention.log) |
| Actual Edge | [Browser checks](competition/verified/browser/edge.log) · [Candidate workspace](competition/verified/screenshots/fixture-candidate-workspace.png) · [Provider status](competition/verified/screenshots/provider-status.png) |
| Upgrade retention | [P09.1 direct](competition/migration-from-p091/upgrade/retention.log) · [Prior R01](competition/migration/upgrade/retention.log) |
| Issues found and repaired | [Independent run](competition/odoo/security/contention.log) · [Reorder diagnosis](competition/reorder-focused.log) · [Deadline-focused rerun](competition/deadline-verified.log) |

## Release 20.0.9.1.4

| Evidence | Artifact |
|---|---|
| Standalone and prior stress parity | [Unit suite](source-closure/standalone.log) · [Source scan](source-closure/source.log) · [P09.1 parity](source-closure/stress-parity.log) |
| Automatic comparison, adjustment and resolution | [Fresh install](source-closure/verified/installation/fresh.log) · [Update](source-closure/verified/installation/upgrade.log) · [Focused rerun](source-closure/last-focused-final.log) |
| PostgreSQL and Edge | [Concurrency](source-closure/verified/security/contention.log) · [Browser](source-closure/verified/browser/edge.log) · [Comparison verification screenshot](source-closure/verified/screenshots/comparison-source-review.png) |
| Populated upgrades | [Direct P09.1](source-closure/migration-from-p091/upgrade/retention.log) · [Previous R01](source-closure/migration/upgrade/retention.log) |
| Initial failures kept | [Calendar source validation](source-closure/odoo/installation/fresh.log) · [Uncommitted browser input](source-closure/release/browser/edge.log) |

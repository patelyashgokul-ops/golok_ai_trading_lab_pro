# P04 command and evidence inventory

Commands ran from the addon root against disposable databases. In the Python commands, `python` is the existing Odoo virtual environment interpreter.

| Execution | Command | Exit | Evidence |
|---|---|---:|---|
| B-U | `python -B -m unittest discover -s tests -p 'unit_*.py' -v` on preserved P03 | 0 | [21 cases, 0.040 s](baseline/unit.log) |
| B-R | `python -B scripts/reproduce_p03.py` on preserved P03 | 0 | [Synthetic result](baseline/replay.json) |
| B-S | `python -B scripts/check_source.py` on preserved P03 | 0 | [Scan](baseline/source.log) |
| B-O, B-C, B-UI | `./.local-test/p03-addons/golok_ai_trading_lab_pro/scripts/verify_odoo.ps1 -Browser -PostgresPort 55494 -HttpPort 18094 -Database golok_p04_baseline_p03` | 0 | [Fresh and upgrade](baseline/odoo/installation), [contended operations](baseline/odoo/security/contention.log), [Edge](baseline/odoo/browser/edge.log). Fresh 34.19 s, contention 7.79 s, Edge 55.03 s. |
| P-U | `python -B -m unittest discover -s tests -p 'unit_*.py' -v` on P04 | 0 | [25 cases, 0.096 s](unit/python.log) |
| P-O, P-C, P-UI | `./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p04/release -Database golok_p04_release -HttpPort 18088` | 0 | [Fresh and upgrade](release/installation), [concurrency](release/security/contention.log), [Edge](release/browser/edge.log). Fresh 47.74 s, contention 7.13 s, Edge 52.96 s. |
| P-M, P-P | `./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p04_baseline_p03 -SourceVersion 20.0.3.0.0 -TargetVersion 20.0.4.0.0 -TargetDatabase golok_p04_migration_p03 -EvidenceDir docs/evidence/p04/migration -ClusterDir .local-test/p03-addons/golok_ai_trading_lab_pro/.local-test/pg -PostgresPort 55494` | 0 | [Migration 12.92 s](migration/upgrade/retention.log), [ORM benchmark 4.11 s](migration/performance/orm.json) |
| P-Q | `./scripts/verify_p04_quota.ps1` | 0 | [Three independent worker quota races](quota.log) |
| P-S | `python -B scripts/check_source.py` | 0 | [Runtime scan](source-scan.log) |
| P-R | `python -B scripts/reproduce_p03.py` on P04 | 0 | [Synthetic ST-01 replay and exact virtual ledger](replay.json) |

An intermediate fresh install returned an error for a field selection policy. That attempt is recorded separately; all final executions passed after repair. Expected duplicate/exclusion exceptions in final PostgreSQL logs are assertions and are rolled back.

# P03 exact execution inventory

Run from the addon root in PowerShell. Python refers to `C:/PycharmProjects/odoo20/.venv/Scripts/python.exe`. The verification and migration harnesses use only disposable loopback databases. No production data or live credentials were loaded in these commands.

| Command | Final result | Evidence |
|---|---|---|
| `python -B -m unittest discover -s tests -p 'unit_*.py' -v` on the P02 source before changes | Exit 0, 18 tests, 0.029 s | [Python log](baseline/unit.log) |
| `python -B scripts/check_source.py` on preserved P02 | Exit 0 | [Source check](baseline/source-scan.log) |
| `python -B scripts/run_backtest.py tests/fixtures/p02/spec.json tests/fixtures/p02/candles.csv` on preserved P02 | Exit 0 | [Replay output](baseline/synthetic.json) |
| `./.local-test/p02-addons/golok_ai_trading_lab_pro/scripts/verify_odoo.ps1 -Browser -PostgresPort 55493 -HttpPort 18093 -Database golok_p03_baseline_p02` | Six fresh ORM, six upgrade ORM, two independent DB scenarios and six browser checks passed. Baseline stage wall times were not preserved separately. | [Runtime retest](baseline/p02-retest) |
| `python -B -m unittest discover -s tests -p 'unit_*.py' -v` on P03 | Exit 0, 21 tests, 0.037 s | [Python log](unit/python.log) |
| `./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p03/final -Database golok_p03_final -HttpPort 18087` | Exit 0. Fresh 49.12 s, upgrade 15.34 s, contention 6.15 s, browser 50.22 s. | [Fresh](final/installation/fresh.log) · [Upgrade](final/installation/upgrade.log) · [Concurrency](final/security/contention.log) · [Edge](final/browser/edge.log) |
| `./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p03/release -Database golok_p03_release -HttpPort 18087` | Exit 0. Fresh 57.40 s, independent contention 6.44 s, browser 74.66 s. Runner logs record ten fresh and ten upgrade cases and eight browser checks. | [Fresh](release/installation/fresh.log) · [Upgrade](release/installation/upgrade.log) · [Concurrency](release/security/contention.log) · [Edge](release/browser/edge.log) |
| `./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p03_baseline_p02 -TargetDatabase golok_p03_migration_preserved_p02 -SourceVersion 20.0.2.0.0 -ClusterDir .local-test/p02-addons/golok_ai_trading_lab_pro/.local-test/pg -PostgresPort 55493` | Exit 0, retained 180 XML IDs and record hashes. Migration 14.47 s. ORM benchmark 4.98 s. | [Retention](migration/upgrade/retention.log) · [Performance](migration/performance/orm.json) |
| `python -B scripts/reproduce_p03.py` | Exit 0. Two completed synthetic replay trades and six independently reconciling virtual events. | [Replay and ledger](backtesting/synthetic-replay-ledger.json) |
| `python -B scripts/check_source.py` | Exit 0, 33 runtime files inspected | [Source check](release/security/source-scan.log) |

The earlier expanded install in `verification/installation/fresh.log` exposed one translation-variable shadowing error in offline diagnostics. The final run above exercised and passed the repaired case. A predecessor core-only run is in `core/`. Expected duplicate SQL errors in test logs are deliberate assertions.

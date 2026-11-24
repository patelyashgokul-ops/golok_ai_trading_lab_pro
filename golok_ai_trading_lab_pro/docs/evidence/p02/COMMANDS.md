# P02 execution index

Commands ran from the module workspace under PowerShell. Python commands used `C:/PycharmProjects/odoo20/.venv/Scripts/python.exe`. Odoo was loaded from `C:/PycharmProjects/odoo20/odoo-20.0`. Test servers were bound to loopback.

| Final execution | Exit | Elapsed | Evidence |
|---|---:|---:|---|
| P01 source `python -B -m unittest discover -s tests -p "unit_*.py" -v` | 0 | 0.004 s runner | [Baseline audit](baseline/audit.log) |
| Archived `./.local-test/p01-addons/golok_ai_trading_lab_pro/scripts/verify_odoo.ps1 -Browser -PostgresPort 55491 -HttpPort 18091 -Database golok_p02_p01_serial` | 0 | 45.65 s fresh, 11.94 s upgrade, 8.63 s contention, 49.78 s browser | [Fresh](baseline/p01-fresh.log) · [Upgrade](baseline/p01-upgrade.log) · [Contention](baseline/p01-contention.log) · [Browser](baseline/browser.log) |
| `python -B -m unittest discover -s tests -p "unit_*.py" -v` | 0 | 0.038 s runner | [P02 unit](unit/python.log) |
| `./scripts/verify_odoo.ps1 -Browser -Database golok_p02_isolated` | 0 | 40.56 s fresh, 12.25 s upgrade, 5.78 s contention, 51.73 s browser | [Fresh](installation/fresh.log) · [Upgrade](installation/upgrade.log) · [Contention](security/contention.log) · [Browser](browser/edge.log) |
| `./scripts/verify_p01_upgrade.ps1` | 0 | 15.29 s Odoo migration; 5.25 s measured 50-instrument workload | [Record retention](upgrade/retention.log) · [Benchmark](performance/orm.json) |
| `python -B scripts/run_backtest.py tests/fixtures/p02/spec.json tests/fixtures/p02/candles.csv` | 0 | Wall time not instrumented | [Deterministic synthetic output](backtesting/synthetic.json) |
| `python -B scripts/check_source.py` | 0 | Wall time not instrumented | [Runtime source inspection](security/source-scan.log) |

Retained earlier attempt logs include a stalled pipeline recovery and a P01 Edge session disconnect. The final recorded executions above ran directly and passed. This folder has no authenticated external integration evidence or licensed financial dataset.

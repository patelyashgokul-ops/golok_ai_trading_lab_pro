# P06–P07 test execution

| Verification | Command or entry point | Observed outcome |
|---|---|---|
| P09.1 baseline | Archive SHA-256, CRC, full and source manifests, source and report parity | 668 archived entries, 667 full manifest entries and 95 source entries matched. The read-only source checkpoint was created. |
| Baseline and final standalone | `python -B -m unittest discover -s tests -p 'unit_*.py' -v` | 52 baseline and 58 final tests passed. |
| Runtime source checks | `python -B scripts/check_source.py` | 68 source files inspected, Python/XML syntax passed and prohibited order and literal credential patterns were absent. |
| P09.1 stress checksum | `scripts.reproduce_p09_stress.stress` | All eleven output scenarios matched their archived results. |
| Strategy and level policy comparison | `scripts.reproduce_p06.run` and the three policies through `services.portfolio.replay` | Five strategies reran. The common fixture produced zero structure trades, three fixed-4R fills with −₹186.06 net and zero ATR-capped trades. Reversing asset and policy input order preserved results. |
| Fresh Odoo and module update | `scripts/verify_odoo.ps1 -Browser` | 25 ORM tests reported with no failures or errors per stage. Includes Upstox fixture ingestion and automatic source conflict protection. |
| Populated upgrade | `scripts/verify_p01_upgrade.ps1 -SourceVersion 20.0.9.1.0 -TargetVersion 20.0.9.1.1` | Preserved 1,243 existing XML IDs, record-level table hashes and immutable snapshot digests on an independent clone. |
| PostgreSQL independent processes | `scripts/verify_contention.py` through the harness | Import, range exclusion, reserve, closure, holdout, scheduler and restart scenarios passed, including actual worker termination and exactly-once retry in test transactions. |
| Microsoft Edge | `scripts/verify_browser.py` through the harness | 20 existing browser scenarios passed. Screenshots are included. |
| Populated-clone performance | `scripts/measure_odoo_p02.py` through upgrade harness | 3,750 synthetic bars across 50 instruments, about 6.34 seconds total, and approximately 148 MB peak process RSS. |
| Offline Upstox performance | Injected V3 JSON with 50 complete 375-bar sessions | 18,750 observations. Approximately 5.38 seconds parsing and 4.18 seconds session validation with Python allocation tracking enabled. |
| Genuine provider and financial checks | No account request made | Unavailable without owner entitlement, an authorized sample and independent costs. |

The early numerical fixture run failed two tests because the adopted historical example contained too few bars for ATR warm-up. The corrected independent 18-bar fixture passed the complete standalone suite. Expected SQL rejection messages in ORM logs correspond to asserted uniqueness and exclusion tests.

[Commands, raw logs and screenshots](evidence/p06_p07_repair/INDEX.md)

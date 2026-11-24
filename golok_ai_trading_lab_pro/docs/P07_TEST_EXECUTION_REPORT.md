# P07 test execution

Windows, Odoo 20 Community, PostgreSQL 18.4, Python 3.11.9 for unit tests and Python 3.14.6 for Odoo. Edge ran on a disposable loopback instance. Evidence is under `docs/evidence/p07`.

```powershell
python -B -m unittest discover -s tests -p 'unit_*.py' -v
python -B scripts/check_source.py
./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p06 -EvidenceDir docs/evidence/p07/release -PostgresPort 55497 -HttpPort 18097 -Database golok_p07_fresh_a
./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p06_fresh_b -TargetDatabase golok_p05_migration_p07 -SourceVersion 20.0.6.0.0 -TargetVersion 20.0.7.0.0 -EvidenceDir docs/evidence/p07/migration -ClusterDir .local-test/pg -PostgresPort 55496
```

42 unit tests passed, covering causal targets, simultaneous-candidate order independence, UDiFF negatives and prior fixtures. Fresh and update ORM each passed 15 tests. Expected constraint violations demonstrate rejection and rollback. PostgreSQL independent connections verified candle, mapping, virtual paper and holdout contention. The migration kept 792 existing XML IDs and checked row hashes. The inherited benchmark measured 3,750 bars across 50 instruments in 4.16 seconds with approximately 142 MiB sampled peak resident memory. Browser results and screenshots are in the release evidence directory.

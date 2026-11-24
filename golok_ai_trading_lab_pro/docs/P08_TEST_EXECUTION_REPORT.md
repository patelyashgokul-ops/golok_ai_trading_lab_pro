# P08 test execution

Environment was Windows, Odoo 20 Community, PostgreSQL 18.4, Python 3.11.9 for standalone tests and Python 3.14.6 in Odoo. Edge ran against a disposable local database. No real user database, broker account or market data was used.

| Execution | Result | Evidence under docs/evidence/p08 |
| --- | --- | --- |
| P07 baseline | CRC, external digest, source and full manifests, 42 tests and both existing replay outcomes verified | baseline/ |
| P08 pure tests | 44 passed | unit.log |
| Runtime scan | 58 files checked. Syntax and fixed read-only scope checks passed | source-check.log |
| First install | Odoo rejected dynamic boolean domain because its search values use a normalized collection | release/installation/fresh.log |
| Second install | ORM supplemental-view regression exposed missing compute on the search-only authorization flag. SQL search worked, but record-level checks denied a valid fixture. | verified/installation/fresh.log |
| Final ORM | Both direct record and SQL search paths verified. Fresh install and update ran 16 cases each. | final/installation/ |
| Independent connections and forced restart | A live PostgreSQL lock was skipped. The separate test process was terminated while holding an uncommitted change, then the queue produced one result. Existing holdout and virtual account races also passed. | final/security/contention.log |
| Populated migration and benchmark | Upgraded a populated P07 test clone and preserved historical XML IDs and row hashes. The benchmark used 50 instruments and 3,750 synthetic bars. | migration-final/ |
| Edge | Login, local import, charts, holdout, list drill-downs and database-backed fixture operations exercised | final/browser/edge.log and final/screenshots/ |

### Reproduction commands

    python -B -m unittest discover -s tests -p 'unit_*.py' -v
    python -B scripts/check_source.py
    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/final -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_c
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08b -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.0.0 -EvidenceDir docs/evidence/p08/migration-final -ClusterDir .local-test/pg-p06 -PostgresPort 55497

Earlier attempts used suffixes a and b for fresh databases. Their logs remain in the archive. Repeated tests should use new disposable database names.

P08.1 reran the full local workflow after adding holdout read protections and seven-day recovery. ORM tests assert sealed candle search, direct read and export denial. They also recover one missed post-market phase with the original session cutoff. End-to-end evidence is under completion and migration-completion.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/completion -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_d
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08c -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.1.0 -EvidenceDir docs/evidence/p08/migration-completion -ClusterDir .local-test/pg-p06 -PostgresPort 55497

The subsequent historical-contract revision adds two standalone tests, bringing the suite to 46. It separates market close, publication and execution on authored fixtures, rejects missing provenance and ensures audit context cannot override decision gates. Local regression and upgrade evidence for this revision is under replay-contract and migration-replay.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/replay-contract -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_e
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08d -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.1.0 -EvidenceDir docs/evidence/p08/migration-replay -ClusterDir .local-test/pg-p06 -PostgresPort 55497

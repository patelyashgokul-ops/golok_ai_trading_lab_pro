# P08 test execution

Environment was Windows, Odoo 20 Community, PostgreSQL 18.4, Python 3.11.9 for standalone tests and Python 3.14.6 in Odoo. Edge ran against a disposable local database. No real user database, broker account or market data was used.

| Execution | Result | Evidence under docs/evidence/p08 |
| --- | --- | --- |
| P07 baseline | CRC, external digest, source and full manifests, 42 tests and both existing replay outcomes verified | baseline/ |
| P08 pure tests | 47 passed | unit.log |
| Runtime scan | 61 files checked. Syntax and fixed read-only scope checks passed | source-check.log |
| First install | Odoo rejected dynamic boolean domain because its search values use a normalized collection | release/installation/fresh.log |
| Second install | ORM supplemental-view regression exposed missing compute on the search-only authorization flag. SQL search worked, but record-level checks denied a valid fixture. | verified/installation/fresh.log |
| Final ORM | Fresh install and update ran 20 cases each. Authorized replay, nested export, revocation and historical publication evidence were tested with authored contract data. | sealed-publication/installation/ |
| Independent connections and forced restart | A separate worker holding an uncommitted change was terminated. The queue produced one result after retry. A committed expired lease was also recovered. | sealed-publication/security/contention.log |
| Populated migration and benchmark | Upgraded a populated P07 test clone and preserved 802 historical XML IDs and row hashes. The benchmark used 50 instruments and 3,750 synthetic bars. | migration-authorized-replay/ |
| Edge | 17 checks covered local import, charts, holdout, list drill-downs and fixture generation and replay. | sealed-publication/browser/edge.log and sealed-publication/screenshots/ |

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

P08.2 exercises active revocation, fixed-term expiry, transient-only denial, nested exports, persisted comparison and research vetoes on conflicting OHLCV. The first run correctly denied export at Odoo's global export privilege before reaching the module-specific gate. The final tests grant test users the global privilege so they specifically exercise the module denial. Evidence is under rights-lifecycle and integrity-release.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/integrity-release -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_g
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08f -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.2.0 -EvidenceDir docs/evidence/p08/migration-integrity -ClusterDir .local-test/pg-p06 -PostgresPort 55497

The daily-completeness regression mixes Legacy CM and targeted UDiFF authored files on one effective mapping, checks the missing middle session, backfills it and verifies the earlier snapshot remains unchanged.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/daily-completeness -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_h

P08.3 verifies committed lease expiry and recovery, rejection of an obsolete worker token and idempotent retry and cancellation. The first run found a stale in-memory state after retry switched the database row back to queued. The retry and cancel actions now refresh the affected Odoo cache fields. The failed run is retained under durable-release.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/final-durable -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_j
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08g -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.3.0 -EvidenceDir docs/evidence/p08/migration-durable -ClusterDir .local-test/pg-p06 -PostgresPort 55497

The owner-controls run adds administrator-only manual check, pause and resume, and a split exceptional session. Fixtures verify a closed-day report and a maintenance period with no research run.

    ./scripts/verify_odoo.ps1 -ClusterDir .local-test/pg-p06 -EvidenceDir docs/evidence/p08/owner-controls -PostgresPort 55497 -HttpPort 18097 -Database golok_p08_fresh_k

P08.4 tests deterministic fixture generation, duplicate requests, rejection of forged lineage and protection against ordinary candle imports. Edge uses the native calendar button and opens the generated dataset's fingerprint.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/generated-fixture -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_l
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08h -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.4.0 -EvidenceDir docs/evidence/p08/migration-fixture -ClusterDir .local-test/pg-p06 -PostgresPort 55497
    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/lineage-release -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_m
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08i -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.5.0 -EvidenceDir docs/evidence/p08/migration-lineage -ClusterDir .local-test/pg-p06 -PostgresPort 55497

The populated P07 clone held six simulation datasets. The migration retained their references and classified all six as simulation. A separate ORM case represents an old market record by removing its review and publication assertions on a disposable test transaction. The first assertion expected the whole metadata row to be hidden and failed. The corrected case verifies that metadata remains available while candles and research are denied.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/lineage-final -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_n

P08.6 tests linked daily corrections, preservation of the original candles, exact retries, and rejection of a predecessor from a different session. It also tests the Odoo historical timing fixture and its frozen dataset fingerprint. The first daily validation run exposed a Python name collision between the translation function and a local unpacked value. The corrected run preserves both the rejection and successful normalization cases.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/revisions-final -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_p
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08k -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.6.0 -EvidenceDir docs/evidence/p08/migration-revisions-final -ClusterDir .local-test/pg-p06 -PostgresPort 55497

P08.7 adds the verified-publication Odoo route. Its authored contract case exercises denied use before attestation, an altered file, analyst attempts to attest, idempotent approval, frozen inputs, execution, nested export denial and revocation. The first run found that injecting defaults for group-restricted fields blocked ordinary dataset creation. The fix strips those context defaults and assigns empty fields only for the permitted role.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/replay-rights-final -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_r
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p07_fresh_a -TargetDatabase golok_p05_migration_p08l -SourceVersion 20.0.7.0.0 -TargetVersion 20.0.8.7.0 -EvidenceDir docs/evidence/p08/migration-authorized-replay -ClusterDir .local-test/pg-p06 -PostgresPort 55497

The next run found that the dataset freeze check was on the quarantine button instead of the shared candle import path. The fix moved the check and its row lock to that shared path.

    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p08/sealed-publication -PostgresPort 55498 -HttpPort 18098 -Database golok_p08_fresh_s

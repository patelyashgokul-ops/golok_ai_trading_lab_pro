# P06 test execution

Evidence is under `docs/evidence/p06`. Runs used disposable local databases. P05 archive checks, source checks, tests and financial fixture outputs are separate from external market validation.

| Execution | Expected and observed | Evidence |
| --- | --- | --- |
| Standalone Python | 39 passing cases across the original suites and new CSV/ZIP, permission, MCP, comparison and strategy cases | unit.log |
| Odoo fresh install and update | 14 test methods in each phase, including grant denial, expiry replacement by new review, quarantined import, five-strategy wizard, walk-forward and holdout | verified/installation/ |
| PostgreSQL concurrency | Independent sessions contend on candle insertion, instrument ranges, paper posting and final holdout consumption | verified/security/contention.log |
| Edge | Actual Odoo login, CSV wizard, chart and mobile overview, drill-downs, retry, company portfolio economics and daily-file form | verified/browser/edge.log and verified/screenshots/ |
| Migration | Populated P05 clone retained 693 XML IDs, 51 candles, one portfolio, three ledger events and comparison hashes | migration/upgrade/retention.log |
| Quotas | Two independent worker connections, one committed reservation for each of three operations | quota.log |
| Performance | 50 instruments, 3,750 synthetic bars. Elapsed 5.79 seconds, sampled peak process memory about 142 MiB, company count 5.4 ms | migration/performance/orm.json |
| Research accounting | Five strategies on the same three synthetic instruments for baseline and doubled tariff rates. Every result reconciled gross less fees, cash and ledger | strategy-competition.json |
| Runtime inspection | Python/XML parsed and fixed read-only operation scan passed | source-check.log |

Run the following commands at the addon root. The first two disposable install rehearsals used `golok_p06_fresh_a` and `golok_p06_fresh_b`. Their evidence is in `release/` and `final/`. The release verification used the following invocations.

```powershell
python -B -m unittest discover -s tests -p 'unit_*.py' -v
python -B scripts/check_source.py
python -B scripts/reproduce_p06.py
./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p06 -EvidenceDir docs/evidence/p06/verified -PostgresPort 55497 -HttpPort 18097 -Database golok_p06_fresh_c
./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p05_fresh_d -TargetDatabase golok_p05_migration_p06a -SourceVersion 20.0.5.0.0 -TargetVersion 20.0.6.0.0 -EvidenceDir docs/evidence/p06/migration -ClusterDir .local-test/pg -PostgresPort 55496
./scripts/verify_p04_quota.ps1 -Database golok_p05_migration_p06a -Cluster .local-test/pg -PostgresPort 55496 -Evidence docs/evidence/p06/quota.log
```

Use a new disposable target database for repeated installation and migration tests. The source database must be an installed, populated P05 test database. The migration benchmark does not measure worst-case portfolio throughput or hotspot performance. Security testing covered ACLs, scoped roles, synthetic input rejection and source operation checks.

# P09 local test execution

The host reported Windows, eight logical processors, 16,918,601,728 bytes of physical memory and Python 3.11.9 for standalone tests. Odoo and Edge use disposable local databases. The hardware inventory uses operating-system APIs because CIM access was restricted. [Environment](evidence/p09/environment.log)

The P08 archive, both manifests, protected source checkpoint and archived synthetic target policies passed independent verification. Its standalone suite finished before changes. [Baseline](evidence/p09/baseline.log) · [Baseline tests](evidence/p09/baseline-unit.log)

The first cycle test found that the Odoo root user is inactive. Jobs now run as the active administrator who created the watch. The second run exposed an unflushed terminal state before an immediate SQL queue lookup. The shared runner now flushes that field and the outcome publisher rejects any attempt to replace a frozen digest. The first contention harness also needed its disposable-database allowlist to include P09. A later fixture worker could not locate Odoo through its namespace package. It now resolves the Odoo executable from the loaded CLI module. Failed logs remain in the evidence directory.

| Check | Evidence under docs/evidence/p09 |
| --- | --- |
| Standalone regression and exact Decimal reference | unit.log |
| Syntax and read-only source scan | source-check.log |
| Fresh Odoo install and update | final/installation |
| Independent PostgreSQL sessions and process termination | final/security |
| Edge native forms | final/browser and final/screenshots |
| Populated P08 migration | migration-final/upgrade |
| 50-instrument reference run | migration-final/performance/orm.json |
| Deterministic doubled-fee comparison | synthetic-stress.json |

Reproduction commands

    python -B -m unittest discover -s tests -p "unit_*.py" -v
    python -B scripts/check_source.py
    python -B scripts/reproduce_p06.py
    ./scripts/verify_odoo.ps1 -Browser -ClusterDir .local-test/pg-p08 -EvidenceDir docs/evidence/p09/final -PostgresPort 55498 -HttpPort 18098 -Database golok_p09_fresh_e
    ./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p08_fresh_s -TargetDatabase golok_p09_migration_b -SourceVersion 20.0.8.7.0 -TargetVersion 20.0.9.0.0 -EvidenceDir docs/evidence/p09/migration-final -ClusterDir .local-test/pg-p08 -PostgresPort 55498

The first populated P08 clone retained all checked records and XML IDs. The synthetic benchmark rejected the new disposable database name until its own allowlist was extended to match the migration harness. Both migration attempts remain documented.

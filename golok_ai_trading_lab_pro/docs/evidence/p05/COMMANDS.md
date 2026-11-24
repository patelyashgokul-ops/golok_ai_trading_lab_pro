# P05 verification commands

Run from the addon root unless specified. Local Odoo commands use disposable PostgreSQL databases. Ports 55495 and 55496 bind to loopback. The Odoo harness generates a test-only browser password in memory.

| ID | Expected check | Actual outcome | Exit | Evidence |
| --- | --- | --- | --- | --- |
| B01 | Archived standalone regression | 25 passed | 0 | baseline/unit.log |
| B02 | Archived fresh, update, contention and browser checks | 11 fresh, 11 update and 9 browser assertions passed, including repeated PostgreSQL races | 0 | baseline/odoo/ |
| B03 | Prior evidence manifests and P04 checkpoint | All entries verified | 0 | baseline/hash.log |
| B04 | Archived source inspection | 36 runtime files checked | 0 | baseline/source.log |
| B05 | Archived replay | Deterministic synthetic replay reproduced | 0 | baseline/replay.json |
| I01 | Initial P05 shell and browser run | 12 fresh, 12 update and 10 browser assertions passed | 0 | verification/ |
| I02 | Intermediate P05 ORM run | Mocked test context malformed | 1 | intermediate/orm-auth-test.log |
| I03 | Intermediate P05 ORM run | The test detected a stale alias to the shared provider cache | 1 | intermediate/orm-session-cache.log |
| F01 | Standalone regression and P05 tests | 34 passed | 0 | unit/python.log |
| F02 | Fresh, update, PostgreSQL contention and Edge | 13 fresh, 13 update and 11 Edge assertions passed | 0 | release/ |
| F03 | Populated P04 upgrade and ORM benchmark | Preserved 564 XML IDs and row hashes. Benchmark processed 3,750 bars | 0 | upgrade-final/ |
| F04 | Independent quota races | One committed reservation per operation; immediate retry denied | 0 | security/quota.log |
| F05 | Deterministic portfolio and independent accounting | Independent arithmetic, explicit veto and two byte-identical replays passed | 0 | portfolio/ |
| F06 | Runtime parsing and fixed operation inspection | 46 runtime files checked | 0 | security/source.log |

## Baseline

The archived code lives under `.local-test/p04-addons/golok_ai_trading_lab_pro` after extracting `docs/history/P04-source.zip` into that directory. Use that archive for baseline Python source and replay checks.

```powershell
# B01, from the archived addon directory
python -B -m unittest discover -s tests -p 'unit_*.py' -v
# B02, from the active addon root
& ./.local-test/p04-addons/golok_ai_trading_lab_pro/scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p04/retest -PostgresPort 55495 -HttpPort 18095 -Database golok_p05_baseline_p04
# B04 and B05, from the archived addon directory
python -B scripts/check_source.py
python -B scripts/reproduce_p03.py
```

B03 compares SHA-256 for each filename in `docs/evidence/manifest.sha256`, the P02–P04 `manifest.sha256` files and the P04 source checkpoint. The final handoff verification repeats these checks.

## P05

```powershell
# I01
./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p05/verification -PostgresPort 55496 -HttpPort 18096 -Database golok_p05_fresh_a
# I02
./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p05/release -PostgresPort 55496 -HttpPort 18096 -Database golok_p05_fresh_b
# I03
./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p05/release -PostgresPort 55496 -HttpPort 18096 -Database golok_p05_fresh_c
# F01
python -B -m unittest discover -s tests -p 'unit_*.py' -v
# F02
./scripts/verify_odoo.ps1 -Browser -EvidenceDir docs/evidence/p05/release -PostgresPort 55496 -HttpPort 18096 -Database golok_p05_fresh_d
# F03
./scripts/verify_p01_upgrade.ps1 -SourceDatabase golok_p05_baseline_p04 -TargetDatabase golok_p05_migration_b -SourceVersion 20.0.4.0.0 -TargetVersion 20.0.5.0.0 -EvidenceDir docs/evidence/p05/upgrade-final -ClusterDir .local-test/p04-addons/golok_ai_trading_lab_pro/.local-test/pg -PostgresPort 55495
# F04
./scripts/verify_p04_quota.ps1 -Database golok_p05_migration_b -Cluster .local-test/p04-addons/golok_ai_trading_lab_pro/.local-test/pg -PostgresPort 55495 -Evidence docs/evidence/p05/security/quota.log
# F05
python -B scripts/reproduce_p05.py | Set-Content -Encoding utf8 docs/evidence/p05/portfolio/fixture.json
python -B scripts/reproduce_p05.py | Set-Content -Encoding utf8 docs/evidence/p05/portfolio/fixture-repeat.json
(Get-FileHash docs/evidence/p05/portfolio/fixture.json).Hash -eq (Get-FileHash docs/evidence/p05/portfolio/fixture-repeat.json).Hash
# F06
python -B scripts/check_source.py
```

## Independent handoff check

Compare the archive hash against `P05_REVIEW_HANDOFF.zip.sha256`, extract it into an empty review directory and compare the extracted files against the manifests. Each hash is followed by a path relative to the extraction root. The source manifest lists runtime source, fixtures and verification scripts. The evidence manifest lists the P05 evidence files. The archive also contains the prior manifests and source checkpoints.

```powershell
(Get-FileHash P05_REVIEW_HANDOFF.zip -Algorithm SHA256).Hash.ToLowerInvariant()
python -m zipfile -t P05_REVIEW_HANDOFF.zip
foreach ($name in @('manifest.sha256', 'source.sha256')) {
    foreach ($line in (Get-Content "docs/evidence/p05/$name")) {
        $expected, $path = $line -split '  ', 2
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) {
            throw "Hash mismatch for $path"
        }
    }
}
```

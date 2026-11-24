param(
    [string]$Database = 'golok_p04_migration_p03',
    [string]$Cluster = '.local-test/p03-addons/golok_ai_trading_lab_pro/.local-test/pg',
    [string]$OdooRoot = 'C:/PycharmProjects/odoo20/odoo-20.0',
    [string]$Python = 'C:/PycharmProjects/odoo20/.venv/Scripts/python.exe',
    [string]$Postgres = 'C:/Program Files/PostgreSQL/18/bin/pg_ctl.exe',
    [int]$PostgresPort = 55494,
    [string]$Evidence = 'docs/evidence/p04/quota.log'
)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    & $Postgres -D $Cluster -l .local-test/postgres-quota.log -o "-h 127.0.0.1 -p $PostgresPort" -w start
    if ($LASTEXITCODE) { throw 'Could not start the isolated PostgreSQL cluster.' }
    try {
        $addons = "$OdooRoot/addons,$(Resolve-Path ..)"
        "from odoo.addons.golok_ai_trading_lab_pro.scripts.verify_provider_quota import run; run(env)" |
            & $Python -B "$OdooRoot/odoo-bin" shell "--addons-path=$addons" --no-http --data-dir=.local-test/odoo-data --db_host=127.0.0.1 "--db_port=$PostgresPort" --db_user=golok_test -d $Database --logfile=.local-test/p04-quota-server.log |
            Tee-Object $Evidence
        if ($LASTEXITCODE) { throw "Quota regression exited $LASTEXITCODE" }
    } finally {
        & $Postgres -D $Cluster -w stop
    }
} finally {
    Pop-Location
}

param(
    [string]$OdooRoot = 'C:/PycharmProjects/odoo20/odoo-20.0',
    [string]$Python = 'C:/PycharmProjects/odoo20/.venv/Scripts/python.exe',
    [string]$PostgresBin = 'C:/Program Files/PostgreSQL/18/bin',
    [int]$PostgresPort = 55489,
    [string]$Database = ('golok_' + (Get-Date -Format yyyyMMddHHmmss))
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Split-Path $PSScriptRoot -Parent
Push-Location $moduleRoot
try {
    foreach ($directory in @('.local-test', '.local-test/odoo-data', 'docs/evidence/installation')) {
        New-Item -ItemType Directory -Force $directory | Out-Null
    }
    $cluster = Join-Path $moduleRoot '.local-test/pg'
    $serverLog = Join-Path $moduleRoot '.local-test/postgres.log'
    if (!(Test-Path (Join-Path $cluster 'PG_VERSION'))) {
        & "$PostgresBin/initdb.exe" -D $cluster -U golok_test -A trust -E UTF8 --locale=C
        if ($LASTEXITCODE) { throw "initdb exited $LASTEXITCODE" }
    }
    & "$PostgresBin/pg_ctl.exe" -D $cluster -l $serverLog -o "-h 127.0.0.1 -p $PostgresPort" -w start
    if ($LASTEXITCODE) { throw "pg_ctl start exited $LASTEXITCODE" }
    try {
        $addonsPath = "$OdooRoot/addons,$(Split-Path $moduleRoot -Parent)"
        $common = @('-B', "$OdooRoot/odoo-bin", "--addons-path=$addonsPath",
            '--data-dir=.local-test/odoo-data', '--db_host=127.0.0.1', "--db_port=$PostgresPort",
            '--db_user=golok_test', '-d', $Database, '--without-demo=all', '--stop-after-init',
            '--no-http', '--test-tags=/golok_ai_trading_lab_pro')
        foreach ($stage in @(@{ Name = 'fresh'; Flag = '-i' }, @{ Name = 'upgrade'; Flag = '-u' })) {
            $log = "docs/evidence/installation/$($stage.Name).log"
            $logOffset = if (Test-Path $log) { (Get-Item $log).Length } else { 0 }
            $timer = [Diagnostics.Stopwatch]::StartNew()
            & $Python @common $stage.Flag golok_ai_trading_lab_pro "--logfile=$log"
            $code = $LASTEXITCODE
            $timer.Stop()
            Write-Output "$($stage.Name) exit=$code seconds=$($timer.Elapsed.TotalSeconds) database=$Database"
            $file = [IO.File]::OpenRead((Join-Path $moduleRoot $log))
            try {
                $file.Position = $logOffset
                $runOutput = [IO.StreamReader]::new($file).ReadToEnd()
            } finally {
                $file.Dispose()
            }
            $runOutput -split "`n" | Select-String 'Starting TestLab|ERROR|CRITICAL|tests? when loading database'
            if ($code) { throw "Odoo $($stage.Name) exited $code" }
        }
    } finally {
        & "$PostgresBin/pg_ctl.exe" -D $cluster -w stop
    }
} finally {
    Pop-Location
}

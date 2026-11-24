param(
    [string]$OdooRoot = 'C:/PycharmProjects/odoo20/odoo-20.0',
    [string]$Python = 'C:/PycharmProjects/odoo20/.venv/Scripts/python.exe',
    [string]$PostgresBin = 'C:/Program Files/PostgreSQL/18/bin',
    [int]$PostgresPort = 55489,
    [string]$Database = ('golok_' + (Get-Date -Format yyyyMMddHHmmss)),
    [switch]$Browser,
    [string]$EvidenceDir = 'docs/evidence/p02',
    [int]$HttpPort = 18089,
    [string]$Edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Split-Path $PSScriptRoot -Parent
Push-Location $moduleRoot
try {
    $env:GOLOK_EVIDENCE_DIR = $EvidenceDir
    foreach ($directory in @('.local-test', '.local-test/odoo-data', "$EvidenceDir/installation",
        "$EvidenceDir/browser", "$EvidenceDir/screenshots", "$EvidenceDir/security")) {
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
        $common = @("--addons-path=$addonsPath",
            '--data-dir=.local-test/odoo-data', '--db_host=127.0.0.1', "--db_port=$PostgresPort",
            '--db_user=golok_test', '-d', $Database)
        foreach ($stage in @(@{ Name = 'fresh'; Flag = '-i' }, @{ Name = 'upgrade'; Flag = '-u' })) {
            $log = "$EvidenceDir/installation/$($stage.Name).log"
            $logOffset = if (Test-Path $log) { (Get-Item $log).Length } else { 0 }
            $timer = [Diagnostics.Stopwatch]::StartNew()
            & $Python -B "$OdooRoot/odoo-bin" @common --without-demo=all --stop-after-init --no-http `
                --test-tags=/golok_ai_trading_lab_pro:TestLab $stage.Flag golok_ai_trading_lab_pro "--logfile=$log"
            $code = $LASTEXITCODE
            $timer.Stop()
            Write-Output "$($stage.Name) exit=$code seconds=$($timer.Elapsed.TotalSeconds) database=$Database"
            $file = [IO.File]::OpenRead((Resolve-Path $log))
            try {
                $file.Position = $logOffset
                $runOutput = [IO.StreamReader]::new($file).ReadToEnd()
            } finally {
                $file.Dispose()
            }
            $runOutput -split "`n" | Select-String 'Starting TestLab|ERROR|CRITICAL|[0-9] tests when loading|[0-9] errors of'
            if ($code) { throw "Odoo $($stage.Name) exited $code" }
        }
        $timer = [Diagnostics.Stopwatch]::StartNew()
        "from odoo.addons.golok_ai_trading_lab_pro.scripts.verify_contention import run; run(env)" |
            & $Python -B "$OdooRoot/odoo-bin" shell @common --no-http --logfile=.local-test/contention-server.log |
            Tee-Object "$EvidenceDir/security/contention.log"
        $code = $LASTEXITCODE
        Write-Output "contention exit=$code seconds=$($timer.Elapsed.TotalSeconds)"
        if ($code) { throw "PostgreSQL contention test exited $code" }

        if ($Browser) {
            $env:GOLOK_TEST_BROWSER_PASSWORD = [guid]::NewGuid().ToString('N')
            try {
                "import os; env.ref('base.user_admin').password = os.environ['GOLOK_TEST_BROWSER_PASSWORD']; env.cr.commit()" |
                    & $Python -B "$OdooRoot/odoo-bin" shell @common --no-http --logfile=.local-test/browser-seed.log
                if ($LASTEXITCODE) { throw "Browser setup exited $LASTEXITCODE" }

                $start = [Diagnostics.ProcessStartInfo]::new($Python)
                $start.WorkingDirectory = $moduleRoot
                $start.CreateNoWindow = $true
                foreach ($argument in @('-B', "$OdooRoot/odoo-bin") + $common +
                    @('--http-interface=127.0.0.1', "--http-port=$HttpPort", '--logfile=.local-test/browser-server.log')) {
                    $start.ArgumentList.Add($argument)
                }
                $server = [Diagnostics.Process]::Start($start)
                try {
                    $endpoint = "http://127.0.0.1:$HttpPort"
                    for ($attempt = 0; $attempt -lt 40; $attempt++) {
                        try {
                            Invoke-WebRequest "$endpoint/web/login?db=$Database" -TimeoutSec 3 | Out-Null
                            break
                        } catch {
                            if ($server.HasExited -or $attempt -eq 39) { throw }
                            Start-Sleep -Milliseconds 500
                        }
                    }
                    $timer = [Diagnostics.Stopwatch]::StartNew()
                    "Browser check database=$Database" | Tee-Object "$EvidenceDir/browser/edge.log" -Append
                    & $Python -B ./scripts/verify_browser.py $endpoint $Database $Edge 2>&1 |
                        Tee-Object "$EvidenceDir/browser/edge.log" -Append
                    $code = $LASTEXITCODE
                    Write-Output "browser exit=$code seconds=$($timer.Elapsed.TotalSeconds)"
                    if ($code) { throw "Browser verification exited $code" }
                } finally {
                    if (!$server.HasExited) { $server.Kill($true); $server.WaitForExit() }
                    $server.Dispose()
                }
            } finally {
                Remove-Item Env:GOLOK_TEST_BROWSER_PASSWORD
            }
        }
    } finally {
        & "$PostgresBin/pg_ctl.exe" -D $cluster -w stop
    }
} finally {
    Remove-Item Env:GOLOK_EVIDENCE_DIR -ErrorAction SilentlyContinue
    Pop-Location
}

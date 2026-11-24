param(
    [string]$SourceDatabase = 'golok_20261124162731',
    [string]$TargetDatabase = ('golok_p02_migration_' + (Get-Date -Format yyyyMMddHHmmss)),
    [string]$SourceVersion = '20.0.1.0.0',
    [string]$TargetVersion = '20.0.3.0.0',
    [string]$EvidenceDir = 'docs/evidence/p03/migration',
    [string]$ClusterDir = '.local-test/pg',
    [string]$OdooRoot = 'C:/PycharmProjects/odoo20/odoo-20.0',
    [string]$Python = 'C:/PycharmProjects/odoo20/.venv/Scripts/python.exe',
    [string]$PostgresBin = 'C:/Program Files/PostgreSQL/18/bin',
    [int]$PostgresPort = 55489
)

$ErrorActionPreference = 'Stop'
if ($SourceDatabase -notmatch '^golok_[a-z0-9_]+$' -or $TargetDatabase -notmatch '^golok_p0[2345]_migration_[a-z0-9_]+$') {
    throw 'Use only disposable test database names.'
}
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    New-Item -ItemType Directory -Force "$EvidenceDir/upgrade","$EvidenceDir/performance" | Out-Null
    & "$PostgresBin/pg_ctl.exe" -D $ClusterDir -l .local-test/postgres-migration.log -o "-h 127.0.0.1 -p $PostgresPort" -w start
    if ($LASTEXITCODE) { throw "PostgreSQL start exited $LASTEXITCODE" }
    try {
        $connection = @('-h', '127.0.0.1', '-p', "$PostgresPort", '-U', 'golok_test')
        & "$PostgresBin/createdb.exe" @connection -T $SourceDatabase $TargetDatabase
        if ($LASTEXITCODE) { throw "Database clone exited $LASTEXITCODE" }
        function Query([string]$sql) {
            & "$PostgresBin/psql.exe" @connection -d $TargetDatabase -X -qAt -v ON_ERROR_STOP=1 -c $sql
            if ($LASTEXITCODE) { throw "Test query exited $LASTEXITCODE" }
        }
        $revision = "select latest_version from ir_module_module where name='golok_ai_trading_lab_pro' and state='installed'"
        $xml = "select name || ' ' || model || ' ' || res_id from ir_model_data where module='golok_ai_trading_lab_pro' order by name"
        $data = @'
select 'instruments:'||count(*)||':'||md5(string_agg(row(id,company_id,name,symbol,exchange,active)::text,';' order by id)) from golok_lab_instrument
union all select 'datasets:'||count(*)||':'||md5(string_agg(row(id,company_id,instrument_id,name,interval,origin,source)::text,';' order by id)) from golok_lab_dataset
union all select 'candles:'||count(*)||':'||md5(string_agg(row(id,dataset_id,close_time,ingested_at,open_price,high_price,low_price,close_price,volume,quality,processing_version)::text,';' order by id)) from golok_lab_candle
union all select 'runs:'||count(*)||':'||md5(string_agg(row(id,dataset_id,as_of,first_close,last_close,input_digest,engine_version,decision,reason,evidence)::text,';' order by id)) from golok_lab_run
order by 1
'@
        if ((Query $revision) -ne $SourceVersion) { throw "The cloned database must contain release $SourceVersion." }
        $before = @(Query $data)
        $beforeXML = @(Query $xml)
        if ($before.Count -ne 4 -or $beforeXML.Count -lt 20 -or ($before -match '^[^:]+:0:')) {
            throw 'The clone lacks the required populated P01 records.'
        }
        $extra = @{}
        if ($SourceVersion -in @('20.0.4.0.0','20.0.5.0.0','20.0.6.0.0','20.0.7.0.0')) {
            $tables = @('calendar','mapping','tariff','experiment','paper_account','paper_batch','paper_event','findings','sync','research_job')
            if ($SourceVersion -in @('20.0.5.0.0','20.0.6.0.0','20.0.7.0.0')) { $tables += @('sync_plan','sync_task') }
            if ($SourceVersion -eq '20.0.5.0.0') { $tables += @('portfolio') }
            if ($SourceVersion -eq '20.0.6.0.0') { $tables += @('holdout','source_review','daily_import') }
            if ($SourceVersion -eq '20.0.7.0.0') { $tables += @('holdout','daily_import','portfolio') }
            foreach ($table in $tables) {
                $extra[$table] = Query "select count(*) || ':' || coalesce(md5(string_agg(row_to_json(t)::text,';' order by id)), 'empty') from golok_lab_$table t"
            }
        }
        $rightsQuery = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-array['research','upstream','revoked_at','retain_until'])::text,';' order by id)), 'empty') from golok_lab_source_review t"
        if ($SourceVersion -eq '20.0.7.0.0') { $oldRights = Query $rightsQuery }
        $portfolioQuery = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-'target_policy')::text,';' order by id)), 'empty') from golok_lab_portfolio t"
        if ($SourceVersion -eq '20.0.6.0.0') { $oldPortfolio = Query $portfolioQuery }
        $addons = "--addons-path=$OdooRoot/addons,$(Resolve-Path ..)"
        $common = @($addons, '--data-dir=.local-test/odoo-data', '--db_host=127.0.0.1',
                    "--db_port=$PostgresPort", '--db_user=golok_test', '-d', $TargetDatabase)
        $timer = [Diagnostics.Stopwatch]::StartNew()
        & $Python -B "$OdooRoot/odoo-bin" @common --no-http --stop-after-init -u golok_ai_trading_lab_pro "--logfile=$EvidenceDir/upgrade/populated.log"
        $code = $LASTEXITCODE
        $timer.Stop()
        if ($code) { throw "Module upgrade exited $code" }
        $after = @(Query $data)
        if ($SourceVersion -eq '20.0.7.0.0' -and (Query $rightsQuery) -ne $oldRights) {
            throw 'Historical source review retention failed.'
        }
        if ($SourceVersion -eq '20.0.6.0.0' -and (Query $portfolioQuery) -ne $oldPortfolio) {
            throw 'Historical portfolio retention failed.'
        }
        $afterXML = @(Query $xml)
        if ((Query $revision) -ne $TargetVersion -or (Compare-Object $before $after) -or
            @($beforeXML | Where-Object { $_ -notin $afterXML }).Count) {
            throw 'P01 data, XML ID or module version verification failed.'
        }
        $extraLines = foreach ($table in ($extra.Keys | Sort-Object)) {
            $retained = Query "select count(*) || ':' || coalesce(md5(string_agg(row_to_json(t)::text,';' order by id)), 'empty') from golok_lab_$table t"
            if ($retained -ne $extra[$table]) { throw "Historical $table retention failed." }
            "${table}:${retained}"
        }
        @("PASS: upgraded populated clone from $SourceVersion to $TargetVersion in $($timer.Elapsed.TotalSeconds) s",
          "PASS: retained $($beforeXML.Count) existing XML IDs and record-level hashes with immutable snapshot digests") + $before + @($extraLines) |
            Tee-Object "$EvidenceDir/upgrade/retention.log"
        "from odoo.addons.golok_ai_trading_lab_pro.scripts.measure_odoo_p02 import run; run(env)" |
            & $Python -B "$OdooRoot/odoo-bin" shell @common --no-http --logfile=.local-test/benchmark-p02.log |
            Tee-Object "$EvidenceDir/performance/orm.json"
        if ($LASTEXITCODE) { throw "Benchmark exited $LASTEXITCODE" }
    } finally {
        & "$PostgresBin/pg_ctl.exe" -D $ClusterDir -w stop
    }
} finally {
    Pop-Location
}

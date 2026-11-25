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
if ($SourceDatabase -notmatch '^golok_[a-z0-9_]+$' -or $TargetDatabase -notmatch '^golok_p0[23459]_migration_[a-z0-9_]+$') {
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
        $lineageFields = @'
select md5(string_agg(row(id, to_jsonb(d)->>'source_review_id', to_jsonb(d)->>'publication_basis')::text,
                      ';' order by id)) from golok_lab_dataset d
'@
        $lineageUpgrade = $TargetVersion -in @('20.0.8.5.0', '20.0.8.6.0', '20.0.8.7.0')
        $revisionUpgrade = $SourceVersion -eq '20.0.7.0.0' -and $TargetVersion -in @('20.0.8.6.0', '20.0.8.7.0')
        if ($lineageUpgrade) { $beforeLineage = Query $lineageFields }
        if ($before.Count -ne 4 -or $beforeXML.Count -lt 20 -or ($before -match '^[^:]+:0:')) {
            throw 'The clone lacks the required populated P01 records.'
        }
        $extra = @{}
        if ($SourceVersion -in @('20.0.4.0.0','20.0.5.0.0','20.0.6.0.0','20.0.7.0.0')) {
            $tables = @('calendar','mapping','tariff','experiment','paper_account','paper_batch','paper_event','findings','sync','research_job')
            if ($SourceVersion -in @('20.0.5.0.0','20.0.6.0.0','20.0.7.0.0')) { $tables += @('sync_plan','sync_task') }
            if ($SourceVersion -eq '20.0.5.0.0') { $tables += @('portfolio') }
            if ($SourceVersion -eq '20.0.6.0.0') { $tables += @('holdout','source_review','daily_import') }
            if ($SourceVersion -eq '20.0.7.0.0') { $tables = @($tables | Where-Object { $_ -ne 'research_job' }) + @('holdout','daily_import','portfolio') }
            foreach ($table in $tables | Where-Object { $_ -notin @('portfolio', 'daily_import') -or -not $revisionUpgrade }) {
                $extra[$table] = Query "select count(*) || ':' || coalesce(md5(string_agg(row_to_json(t)::text,';' order by id)), 'empty') from golok_lab_$table t"
            }
        }
        $revisionDigestSql = @{}
        if ($revisionUpgrade) {
            $revisionDigestSql['portfolio'] = "select md5(string_agg((to_jsonb(t)-array['contract_fixture','historical_authorized'])::text,';' order by id)) from golok_lab_portfolio t"
            $revisionDigestSql['daily_import'] = "select md5(string_agg((to_jsonb(t)-array['corrects_id','correction_evidence','correction_scope'])::text,';' order by id)) from golok_lab_daily_import t"
            $beforeRevision = @{}
            foreach ($table in $revisionDigestSql.Keys) { $beforeRevision[$table] = Query $revisionDigestSql[$table] }
        }
        $rightsQuery = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-array['research','upstream','revoked_at','retain_until','raw_share_ohlcv'])::text,';' order by id)), 'empty') from golok_lab_source_review t"
        if ($SourceVersion -eq '20.0.7.0.0') { $oldRights = Query $rightsQuery }
        $jobQuery = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-array['attempts','lease_until','worker_token','started_at'])::text,';' order by id)), 'empty') from golok_lab_research_job t"
        if ($SourceVersion -eq '20.0.7.0.0') { $oldJobs = Query $jobQuery }
        $portfolioQuery = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-'target_policy')::text,';' order by id)), 'empty') from golok_lab_portfolio t"
        if ($SourceVersion -eq '20.0.6.0.0') { $oldPortfolio = Query $portfolioQuery }
        $p08RecordDigests = @{}
        if ($SourceVersion -eq '20.0.8.7.0') {
            foreach ($table in @('calendar','mapping','tariff','experiment','paper_account','paper_batch','paper_event',
                                 'findings','sync','sync_plan','sync_task','research_job','holdout','source_review',
                                 'daily_import','portfolio','session_event','source_comparison','session_watch')) {
                $digestSql = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)-array['cycle_minutes','paper_account_id'])::text,';' order by id)), 'empty') from golok_lab_$table t"
                $p08RecordDigests[$table] = @{ Sql = $digestSql; Before = (Query $digestSql) }
            }
        }
        if ($SourceVersion -in @('20.0.9.0.0','20.0.9.1.0','20.0.9.1.1','20.0.9.1.2','20.0.9.1.3','20.0.9.1.4','20.0.9.1.5')) {
            $p09Tables = @{
                session_watch = @('paper_account_id')
                session_event = @()
                research_cycle = @()
                research_candidate = @('generated_at')
                fixture_account = @('strategy','target_policy')
                fixture_order = @('candidate_id','dataset_id','expires','limit_price','stop_price','target_price',
                                  'entry_paise','entry_candle_id','last_entry_check_id','exit_candle_id','exit_reason')
                fixture_journal = @()
                performance_report = @()
                walk_experiment = @()
                research_job = @()
                portfolio = @()
                holdout = @()
                source_review = @()
            }
            if ($SourceVersion -ne '20.0.9.0.0') {
                foreach ($table in @('calendar','mapping','sync','sync_plan','sync_task','source_comparison','provider_budget')) {
                    $p09Tables[$table] = @()
                }
                foreach ($table in @($p09Tables.Keys)) { $p09Tables[$table] = @() }
            }
            if ($TargetVersion -eq '20.0.9.1.4') {
                $p09Tables['source_comparison'] = @('replacement_id','resolution_reference','resolved_by','resolved_at')
            }
            if ($TargetVersion -eq '20.0.9.1.5') {
                $p09Tables['findings'] = @('evidence_contract')
                if ($SourceVersion -ne '20.0.9.1.4') {
                    $p09Tables['source_comparison'] = @('replacement_id','resolution_reference','resolved_by','resolved_at')
                }
            }
            if ($SourceVersion -eq '20.0.9.1.5') {
                $p09Tables['findings'] = @()
            }
            if ($TargetVersion -eq '20.0.9.1.6') {
                $p09Tables['sync'] = @('fallback_for_id')
                if ($SourceVersion -ne '20.0.9.1.5') {
                    $p09Tables['findings'] = @('evidence_contract')
                    if ($SourceVersion -ne '20.0.9.1.4') {
                        $p09Tables['source_comparison'] = @('replacement_id','resolution_reference','resolved_by','resolved_at')
                    }
                }
            }
            foreach ($table in $p09Tables.Keys) {
                $exclude = if ($p09Tables[$table].Count) { "-array['" + ($p09Tables[$table] -join "','") + "']" } else { "" }
                $digestSql = "select count(*) || ':' || coalesce(md5(string_agg((to_jsonb(t)$exclude)::text,';' order by id)), 'empty') from golok_lab_$table t"
                $p08RecordDigests[$table] = @{ Sql = $digestSql; Before = (Query $digestSql) }
            }
        }
        $addons = "--addons-path=$OdooRoot/addons,$(Resolve-Path ..)"
        $common = @($addons, '--data-dir=.local-test/odoo-data', '--db_host=127.0.0.1',
                    "--db_port=$PostgresPort", '--db_user=golok_test', '-d', $TargetDatabase)
        $timer = [Diagnostics.Stopwatch]::StartNew()
        & $Python -B "$OdooRoot/odoo-bin" @common --no-http --stop-after-init -u golok_ai_trading_lab_pro "--logfile=$EvidenceDir/upgrade/populated.log"
        $code = $LASTEXITCODE
        $timer.Stop()
        if ($code) { throw "Module upgrade exited $code" }
        $after = @(Query $data)
        $p08Evidence = foreach ($table in ($p08RecordDigests.Keys | Sort-Object)) {
            $entry = $p08RecordDigests[$table]
            $retained = Query $entry.Sql
            if ($retained -ne $entry.Before) { throw "Historical P08 $table retention failed." }
            "${table}:${retained}"
        }
        foreach ($table in $revisionDigestSql.Keys) {
            if ((Query $revisionDigestSql[$table]) -ne $beforeRevision[$table]) { throw "Historical $table retention failed." }
        }
        if ($lineageUpgrade) {
            if ((Query $lineageFields) -ne $beforeLineage) { throw 'Upgrade changed prior dataset authorization or publication evidence.' }
            $lineageClassCounts = @'
select origin, case
    when quarantined or integrity_conflict then 'quarantined'
    when origin = 'synthetic' and fixture_version is not null then 'generated_fixture'
    when origin = 'synthetic' then 'simulation'
    when source_review_id is null or publication_basis is null then 'insufficient'
    else 'bound_review_requires_current_rights'
end as classification, count(*) from golok_lab_dataset
group by 1, 2 order by 1, 2
'@
            @('PASS: prior authorization references and publication assertions preserved.',
              'origin|classification|datasets') + @(Query $lineageClassCounts) |
                Tee-Object "$EvidenceDir/upgrade/dataset-lineage.log"
        }
        if ($SourceVersion -eq '20.0.7.0.0' -and (Query $rightsQuery) -ne $oldRights) {
            throw 'Historical source review retention failed.'
        }
        if ($SourceVersion -eq '20.0.7.0.0' -and (Query $jobQuery) -ne $oldJobs) {
            throw 'Historical research job retention failed.'
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
          "PASS: retained $($beforeXML.Count) existing XML IDs and record-level hashes with immutable snapshot digests") + $before + @($extraLines) + @($p08Evidence) |
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

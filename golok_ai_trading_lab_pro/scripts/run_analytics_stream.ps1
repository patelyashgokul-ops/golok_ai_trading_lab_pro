param(
    [Parameter(Mandatory)][string]$Database,
    [Parameter(Mandatory)][int]$CompanyId,
    [string]$OdooRoot = 'C:/PycharmProjects/odoo20/odoo-20.0',
    [string]$Python = 'C:/PycharmProjects/odoo20/.venv/Scripts/python.exe',
    [Parameter(Mandatory)][string]$Config
)

$ErrorActionPreference = 'Stop'
$moduleRoot = Split-Path $PSScriptRoot -Parent
$configPath = (Resolve-Path -LiteralPath $Config).Path
if ($CompanyId -le 0 -or $Database -notmatch '^[A-Za-z0-9_.-]+$' -or $Database.StartsWith('-')) {
    throw 'Supply an Odoo database name and a positive company ID.'
}
$previous = $env:GOLOK_ANALYTICS_COMPANY_ID
Push-Location $moduleRoot
try {
    $env:GOLOK_ANALYTICS_COMPANY_ID = "$CompanyId"
    'from odoo.addons.golok_ai_trading_lab_pro.scripts.run_analytics_stream import run; run(env)' |
        & $Python -B "$OdooRoot/odoo-bin" shell -c $configPath -d $Database --no-http
    if ($LASTEXITCODE) { throw "Analytics worker exited $LASTEXITCODE" }
} finally {
    $env:GOLOK_ANALYTICS_COMPANY_ID = $previous
    Pop-Location
}

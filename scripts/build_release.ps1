param(
    [string]$Version = "0.9.4"
)
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot\..
try {
    py -3.11 -m build
    $wheel = Get-ChildItem dist\dlss_swapper-$Version-*.whl | Select-Object -First 1
    if (-
param(
    [string]$GodotExecutable
)

$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($GodotExecutable)) {
    $GodotExecutable = Join-Path $repositoryRoot ".tools/godot/Godot_v4.7.2-stable_win64_console.exe"
}

$env:UV_CACHE_DIR = Join-Path $repositoryRoot ".tools/uv/cache"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $repositoryRoot ".tools/uv/python"
$env:UV_PROJECT_ENVIRONMENT = Join-Path $repositoryRoot ".venv"
$env:APPDATA = Join-Path $repositoryRoot ".tools/godot/environment/appdata"
$env:LOCALAPPDATA = Join-Path $repositoryRoot ".tools/godot/environment/localappdata"
$env:TEMP = Join-Path $repositoryRoot ".tools/runtime/temp"
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null

Push-Location $repositoryRoot
try {
    uv sync --locked --all-groups
    if ($LASTEXITCODE -ne 0) { throw "uv sync failed" }
    uv run --locked pytest -q
    if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
    uv run --locked ruff check src tests
    if ($LASTEXITCODE -ne 0) { throw "ruff failed" }
    & (Join-Path $repositoryRoot "scripts/test-lab.ps1") -GodotExecutable $GodotExecutable
    if ($LASTEXITCODE -ne 0) { throw "lab regression failed" }
    $dockLog = Join-Path $repositoryRoot "artifacts/godot-dock-smoke.log"
    & $GodotExecutable --headless --path (Join-Path $repositoryRoot "godot") `
        --script "res://tests/dock_smoke.gd" --log-file $dockLog
    if ($LASTEXITCODE -ne 0) { throw "dock smoke failed" }
}
finally {
    Pop-Location
}

Write-Output "GAMEMAKER_FRAMEWORK_TEST_PASS"

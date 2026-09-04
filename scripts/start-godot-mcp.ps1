. (Join-Path $PSScriptRoot "workspace-environment.ps1")
$providerRoot = Join-Path $gameMakerRoot ".tools/providers/godot-ai-a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e"
$python = Join-Path $providerRoot ".venv/Scripts/python.exe"
if (-not (Test-Path -LiteralPath $python)) { throw "Run prepare-trial.ps1 first" }
Push-Location $providerRoot
try {
    & $python -m godot_ai attach --port 8000 --ws-port 9500
    exit $LASTEXITCODE
} finally { Pop-Location }

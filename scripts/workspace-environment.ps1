$ErrorActionPreference = "Stop"
$gameMakerRoot = Split-Path -Parent $PSScriptRoot
$env:UV_CACHE_DIR = Join-Path $gameMakerRoot ".tools/uv/cache"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $gameMakerRoot ".tools/uv/python"
$env:UV_PROJECT_ENVIRONMENT = Join-Path $gameMakerRoot ".venv"
$env:UV_LINK_MODE = "copy"
$env:APPDATA = Join-Path $gameMakerRoot ".tools/godot/environment/appdata"
$env:LOCALAPPDATA = Join-Path $gameMakerRoot ".tools/godot/environment/localappdata"
$env:TEMP = Join-Path $gameMakerRoot ".tools/runtime/temp"
$env:TMP = $env:TEMP
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:GODOT_AI_DISABLE_TELEMETRY = "true"
# The upstream dev mode disables its release updater; the plugin is an unmodified dependency.
$env:GODOT_AI_MODE = "dev"
foreach ($directory in @($env:UV_CACHE_DIR, $env:APPDATA, $env:LOCALAPPDATA, $env:TEMP)) {
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
}

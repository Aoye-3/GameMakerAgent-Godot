param(
    [string]$GodotExecutable
)

$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$fixtureRoot = Join-Path $repositoryRoot "lab/fixtures/godot-runtime-probe"
$candidateCases = Join-Path $repositoryRoot "lab/candidates/studio-advisor/evals/cases.json"
$sourceManifest = Join-Path $repositoryRoot "lab/sources/upstreams.json"
$artifactRoot = Join-Path $repositoryRoot "artifacts/lab"
$godotEnvironmentRoot = Join-Path $repositoryRoot ".tools/godot/environment"

if ([string]::IsNullOrWhiteSpace($GodotExecutable)) {
    $GodotExecutable = Join-Path $repositoryRoot ".tools/godot/Godot_v4.7.2-stable_win64_console.exe"
}

if (-not (Test-Path -LiteralPath $GodotExecutable -PathType Leaf)) {
    throw "Godot executable not found: $GodotExecutable"
}

if (-not (Test-Path -LiteralPath $candidateCases -PathType Leaf)) {
    throw "Studio Advisor eval cases not found: $candidateCases"
}

if (-not (Test-Path -LiteralPath $sourceManifest -PathType Leaf)) {
    throw "Source manifest not found: $sourceManifest"
}

$casesDocument = Get-Content -Raw -Encoding UTF8 -LiteralPath $candidateCases | ConvertFrom-Json
if ($casesDocument.schema_version -ne "0.1" -or $casesDocument.cases.Count -lt 1) {
    throw "Studio Advisor eval cases do not satisfy the lab intake contract."
}

$sourceDocument = Get-Content -Raw -Encoding UTF8 -LiteralPath $sourceManifest | ConvertFrom-Json
if ($sourceDocument.schema_version -ne "0.1" -or $sourceDocument.sources.Count -lt 1) {
    throw "Source manifest does not satisfy the lab intake contract."
}

New-Item -ItemType Directory -Force -Path $artifactRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $godotEnvironmentRoot "appdata") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $godotEnvironmentRoot "localappdata") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $godotEnvironmentRoot "temp") | Out-Null
$logPath = Join-Path $artifactRoot "godot-runtime-probe.log"

$originalAppDataPath = $env:APPDATA
$originalLocalAppDataPath = $env:LOCALAPPDATA
$originalTempPath = $env:TEMP
$originalTmpPath = $env:TMP

try {
    # Keep Godot data and temporary output on the current workspace drive. The _sc_
    # marker remains the primary portable-mode signal; explicit environment paths
    # also cover Windows console-launcher builds that do not honor it for user://.
    $env:APPDATA = Join-Path $godotEnvironmentRoot "appdata"
    $env:LOCALAPPDATA = Join-Path $godotEnvironmentRoot "localappdata"
    $env:TEMP = Join-Path $godotEnvironmentRoot "temp"
    $env:TMP = Join-Path $godotEnvironmentRoot "temp"

    $version = (& $GodotExecutable --version | Out-String).Trim()
    if (-not $version.StartsWith("4.7.2")) {
        throw "Expected Godot 4.7.2, received: $version"
    }

    # Godot CLI flags follow the official command-line reference:
    # https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html
    & $GodotExecutable `
        --headless `
        --path $fixtureRoot `
        --script "res://tests/runtime_probe_smoke.gd" `
        --log-file $logPath

    if ($LASTEXITCODE -ne 0) {
        throw "Godot runtime probe failed with exit code $LASTEXITCODE. See $logPath"
    }
}
finally {
    $env:APPDATA = $originalAppDataPath
    $env:LOCALAPPDATA = $originalLocalAppDataPath
    $env:TEMP = $originalTempPath
    $env:TMP = $originalTmpPath
}

Write-Output "LAB_TEST_PASS studio_advisor_cases=$($casesDocument.cases.Count) sources=$($sourceDocument.sources.Count) godot=$version"

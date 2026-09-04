param([switch]$CheckOnly)
$ErrorActionPreference = "Stop"
$repository = Split-Path -Parent $PSScriptRoot
$project = Join-Path $repository "Project1/project-1"
if (-not (Test-Path -LiteralPath (Join-Path $project "project.godot") -PathType Leaf)) {
    throw "Native project missing. Create it manually first: $project"
}
$revision = "a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e"
git -C $repository cat-file -e ($revision + ":plugin/addons/godot_ai/plugin.cfg")
if ($LASTEXITCODE -ne 0) { throw "Pinned provider Git object is missing" }
if ($CheckOnly) { Write-Output "TRIAL_PREPARATION_INPUTS_OK $project"; exit 0 }
. (Join-Path $PSScriptRoot "workspace-environment.ps1")
$providerRoot = Join-Path $repository (".tools/providers/godot-ai-" + $revision)
if (-not (Test-Path -LiteralPath $providerRoot)) {
    New-Item -ItemType Directory -Force -Path $providerRoot | Out-Null
    $archive = Join-Path $providerRoot "dependency.zip"
    # Extract only installable dependency components, never a development checkout or project copy.
    git -C $repository archive --format=zip --output=$archive $revision src/godot_ai pyproject.toml README.md LICENSE plugin/addons/godot_ai
    if ($LASTEXITCODE -ne 0) { throw "Dependency archive failed" }
    Expand-Archive -LiteralPath $archive -DestinationPath $providerRoot
}
$manifest = Get-Content -Raw -LiteralPath (Join-Path $repository "adapters/godot-ai/installation.json") | ConvertFrom-Json
$archiveHash = (Get-FileHash -LiteralPath (Join-Path $providerRoot "dependency.zip") -Algorithm SHA256).Hash.ToLowerInvariant()
if ($archiveHash -ne $manifest.archive_sha256) { throw "Pinned dependency archive checksum mismatch" }
$env:UV_PROJECT_ENVIRONMENT = Join-Path $providerRoot ".venv"
if (-not (Test-Path -LiteralPath (Join-Path $providerRoot "uv.lock"))) {
    uv lock --project $providerRoot
    if ($LASTEXITCODE -ne 0) { throw "Provider dependency resolution failed" }
}
uv sync --locked --no-dev --project $providerRoot
if ($LASTEXITCODE -ne 0) { throw "Provider dependency installation failed" }
$links = @{
    (Join-Path $project "addons/godot_ai") = (Join-Path $providerRoot "plugin/addons/godot_ai")
    (Join-Path $project "addons/gamemaker_context") = (Join-Path $repository "godot/addons/gamemaker_context")
}
foreach ($skill in @("studio-advisor", "game-delivery", "evidence-review")) {
    $links[(Join-Path $repository ".agents/skills/$skill")] = Join-Path $repository "plugins/gamemaker-agent/skills/$skill"
}
foreach ($destination in $links.Keys) {
    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Item -LiteralPath $destination
        if ($existing.LinkType -ne "Junction" -or $existing.Target -ne $links[$destination]) {
            throw "Refusing to replace existing path: $destination"
        }
    } else {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
        New-Item -ItemType Junction -Path $destination -Target $links[$destination] | Out-Null
    }
}
Write-Output "TRIAL_COMPONENTS_INSTALLED: enable Godot AI and GameMaker Context in the native editor. MCP connection is NOT yet verified."

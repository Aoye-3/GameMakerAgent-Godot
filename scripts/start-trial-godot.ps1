param([switch]$ProjectManager)
. (Join-Path $PSScriptRoot "workspace-environment.ps1")
$executable = Join-Path $gameMakerRoot ".tools/godot/Godot_v4.7.2-stable_win64.exe"
$project = Join-Path $gameMakerRoot "Project1/project-1"
if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) { throw "Godot 4.7.2 missing" }
if ($ProjectManager) {
    Start-Process -FilePath $executable -WorkingDirectory $gameMakerRoot -ArgumentList "--project-manager" | Out-Null
} else {
    if (-not (Test-Path -LiteralPath (Join-Path $project "project.godot"))) {
        throw "Create the native project in Project Manager first: $project"
    }
    Start-Process -FilePath $executable -WorkingDirectory $project -ArgumentList @("--editor", "--path", ('"' + $project + '"')) | Out-Null
}

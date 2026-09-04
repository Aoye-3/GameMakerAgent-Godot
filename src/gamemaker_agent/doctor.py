"""Read-only readiness diagnostics for the packaged environment."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from .schemas import SchemaCatalog


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def diagnose(project: Path, godot: Path | None = None) -> dict[str, Any]:
    repo = repository_root()
    project = project.resolve()
    godot = godot or repo / ".tools" / "godot" / "Godot_v4.7.2-stable_win64_console.exe"
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("python", sys.version_info >= (3, 11), sys.version.split()[0])
    add("godot_project", (project / "project.godot").is_file(), str(project))
    add("record_access", project.is_dir() and os.access(project, os.R_OK | os.W_OK), str(project))
    add(
        "codex_plugin",
        (repo / "plugins/gamemaker-agent/.codex-plugin/plugin.json").is_file(),
        "plugins/gamemaker-agent",
    )
    skill_root = repo / "plugins/gamemaker-agent/skills"
    skills = ["studio-advisor", "game-delivery", "evidence-review"]
    add(
        "skills",
        all((skill_root / item / "SKILL.md").is_file() for item in skills),
        ", ".join(skills),
    )
    add(
        "godot_dock",
        (project / "addons/gamemaker_context/plugin.cfg").is_file(),
        str(project / "addons/gamemaker_context"),
    )
    profiles = list((repo / "adapters/profiles").glob("*.json"))
    profiles_ok = bool(profiles)
    for profile in profiles:
        import json

        value = json.loads(profile.read_text(encoding="utf-8"))
        profiles_ok = profiles_ok and not SchemaCatalog().validate(
            "provider-capability-profile", value
        )
    add("provider_profiles", profiles_ok, f"{len(profiles)} profile(s)")
    if godot.is_file():
        try:
            version = subprocess.run(
                [str(godot), "--version"], capture_output=True, text=True, timeout=10, check=True
            ).stdout.strip()
            add("godot", version.startswith("4.7.2"), version)
        except (OSError, subprocess.SubprocessError) as exc:
            add("godot", False, str(exc))
    else:
        add("godot", False, f"not found: {godot}")
    return {
        "ready": False,
        "files_ready": all(item["ok"] for item in checks),
        "provider_connected": None,
        "conformance_passed": None,
        "checks": checks,
        "next_action": "Live MCP connection and repeated conformance have not been verified.",
    }

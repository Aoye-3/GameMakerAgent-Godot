"""Read-only readiness diagnostics for the packaged environment."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from .schemas import SchemaCatalog


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def diagnose(project: Path, godot: Path | None = None, *, live: bool = False) -> dict[str, Any]:
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
    result = {
        "ready": False,
        "files_ready": all(item["ok"] for item in checks),
        "provider_connected": None,
        "conformance_passed": None,
        "checks": checks,
        "next_action": "Live MCP connection and repeated conformance have not been verified.",
    }
    if live:
        probe = live_probe(repo, project)
        result['live'] = probe
        result['provider_connected'] = probe.get('connected', False)
        result['conformance_passed'] = conformance_record_valid(project, probe)
        result['ready'] = all((result['files_ready'], result['provider_connected'],
                               result['conformance_passed']))
        result['next_action'] = (
            'Environment connected; use Codex to develop and review current work.'
            if result['ready'] else 'Inspect live errors and recorded conformance.'
        )
    return result


def live_probe(repo: Path, project: Path) -> dict:
    provider = repo / '.tools/providers/godot-ai-a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e'
    try:
        output = subprocess.run(
            [str(provider / '.venv/Scripts/python.exe'),
             str(repo / 'adapters/godot-ai/probe.py'), str(project)],
            capture_output=True, text=True, timeout=35, check=True,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        )
        return json.loads(output.stdout)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return {'connected': False, 'error': str(exc)}


def conformance_record_valid(project: Path, probe: dict) -> bool | None:
    path = project / '.vibegame/gamemaker/conformance.json'
    if not path.is_file():
        return None
    try:
        record = json.loads(path.read_text('utf-8'))
        session = probe.get('session', {})
        if (record['provider_version'] != session.get('plugin_version')
                or Path(record['project']).resolve() != project.resolve()
                or not record.get('reconnected') or len(record['rounds']) < 2):
            return False
        for run in record['rounds']:
            if not run.get('passed') or not run.get('run_id') or not run.get('artifacts'):
                return False
            for artifact in run['artifacts']:
                file = (project / artifact['path']).resolve()
                if (not file.is_relative_to(project.resolve()) or not file.is_file()
                        or hashlib.sha256(file.read_bytes()).hexdigest() != artifact['sha256']):
                    return False
        return True
    except (OSError, ValueError, KeyError, TypeError):
        return False

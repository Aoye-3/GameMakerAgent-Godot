"""Bounded, disposable views over a native Godot project."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

SOURCE_SUFFIXES = {".gd", ".godot", ".tres", ".tscn"}
FINGERPRINT_SUFFIXES = SOURCE_SUFFIXES | {".png", ".svg", ".import", ".uid"}
MAX_FILE_BYTES = 256 * 1024
MAX_FACTS = 20


def _source_files(root: Path) -> Iterable[Path]:
    for directory, folders, files in os.walk(root, followlinks=False):
        folders[:] = sorted(
            name for name in folders if not name.startswith('.')
            and not (Path(directory).name == 'addons' and name in {
                'godot_ai', 'gamemaker_context'
            })
        )
        for name in sorted(files):
            path = Path(directory) / name
            if path.suffix.lower() in FINGERPRINT_SUFFIXES and path.resolve().is_relative_to(root):
                yield path


def project_revision(root: Path) -> str:
    digest = hashlib.sha256()
    for path in _source_files(root):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8") + b'\0')
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return f"sha256:{digest.hexdigest()}"


def _parse_project_settings(text: str) -> dict[str, Any]:
    features_match = re.search(r"^config/features=PackedStringArray\((.*)\)$", text, re.M)
    features = re.findall(r'"([^"]+)"', features_match.group(1)) if features_match else []
    main_match = re.search(r'^run/main_scene="([^"]+)"$', text, re.M)
    section = re.search(r'^\[input\]\s*\n(.*?)(?=^\[|\Z)', text, re.M | re.S)
    inputs = sorted(set(re.findall(r'^([^\s"=]+)\s*=\s*\{', section[1], re.M))) if section else []
    return {
        "features": features,
        "main_scene": main_match.group(1) if main_match else None,
        "input_actions": inputs,
    }


def query_project(root: Path, terms: list[str], max_facts: int = MAX_FACTS) -> dict[str, Any]:
    root = root.resolve()
    revision = project_revision(root)
    project_file = root / "project.godot"
    if not project_file.is_file():
        return {
            "schema_version": "0.1",
            "context_id": f"context-{revision.removeprefix('sha256:')[:12]}",
            "project_state": "non_godot",
            "project_root": str(root),
            "source_revision": revision,
            "engine": {"features": [], "main_scene": None, "input_actions": []},
            "facts": [],
        }

    settings_text = project_file.read_text(encoding="utf-8-sig")
    engine = _parse_project_settings(settings_text)
    if str(engine['main_scene']).startswith('uid://'):
        uid = engine['main_scene']
        for path in _source_files(root):
            if path.suffix == '.tscn' and f'uid="{uid}"' in path.read_text('utf-8-sig')[:1024]:
                engine['main_scene'] = 'res://' + path.relative_to(root).as_posix()
                break
    normalized_terms = [term.casefold() for term in terms if term.strip()]
    facts: list[dict[str, str]] = []

    for action in engine["input_actions"]:
        if not normalized_terms or any(term in action.casefold() for term in normalized_terms):
            facts.append({"kind": "player_verb", "value": action, "source": "project.godot"})

    for path in _source_files(root):
        if path == project_file or path.suffix not in SOURCE_SUFFIXES or len(facts) >= max_facts:
            continue
        relative = path.relative_to(root).as_posix()
        if path.stat().st_size > MAX_FILE_BYTES:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        haystack = f"{relative}\n{text}".casefold()
        if normalized_terms and not any(term in haystack for term in normalized_terms):
            continue
        kind = {".tscn": "scene", ".gd": "script", ".tres": "resource"}.get(
            path.suffix.lower(), "resource"
        )
        facts.append({"kind": kind, "value": relative, "source": relative})

    return {
        "schema_version": "0.1",
        "context_id": f"context-{revision.removeprefix('sha256:')[:12]}",
        "project_state": "godot_project",
        "project_root": str(root),
        "source_revision": revision,
        "git_revision": git_revision(root),
        "engine": engine,
        "facts": facts[:max_facts],
    }


def is_context_stale(context: dict[str, Any], root: Path) -> bool:
    return context.get("source_revision") != project_revision(root.resolve())


def git_revision(root: Path) -> str | None:
    result = subprocess.run(
        ['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None

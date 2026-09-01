"""Bounded, disposable views over a native Godot project."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Iterable

SOURCE_SUFFIXES = {".gd", ".godot", ".tres", ".tscn"}
MAX_FILE_BYTES = 256 * 1024
MAX_FACTS = 20


def _source_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if ".vibegame" in path.parts or ".godot" in path.parts:
            continue
        if path.name == "project.godot" or path.suffix.lower() in SOURCE_SUFFIXES:
            yield path


def project_revision(root: Path) -> str:
    digest = hashlib.sha256()
    for path in _source_files(root):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def _parse_project_settings(text: str) -> dict[str, Any]:
    features_match = re.search(r"^config/features=PackedStringArray\((.*)\)$", text, re.M)
    features = re.findall(r'"([^"]+)"', features_match.group(1)) if features_match else []
    main_match = re.search(r'^run/main_scene="([^"]+)"$', text, re.M)
    inputs = sorted(set(re.findall(r"^\[input/([^\]]+)\]$", text, re.M)))
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
    normalized_terms = [term.casefold() for term in terms if term.strip()]
    facts: list[dict[str, str]] = []

    for action in engine["input_actions"]:
        if not normalized_terms or any(term in action.casefold() for term in normalized_terms):
            facts.append({"kind": "player_verb", "value": action, "source": "project.godot"})

    for path in _source_files(root):
        if path == project_file or len(facts) >= max_facts:
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
        "engine": engine,
        "facts": facts[:max_facts],
    }


def is_context_stale(context: dict[str, Any], root: Path) -> bool:
    return context.get("source_revision") != project_revision(root.resolve())

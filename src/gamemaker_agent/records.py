"""Validated, lightweight project-local production records."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from .delivery import review_work
from .project import project_revision, source_manifest
from .schemas import SchemaCatalog

ARTIFACT_PATHS = {
    "decision-card": "decision-card.json",
    "project-context": "project-context.json",
    "production-card": "production-card.json",
    "implementation-record": "implementation.json",
    "normalized-assets": "normalized-assets.json",
    "evidence-bundle": "evidence/evidence-bundle.json",
}
SAFE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _artifact_path(work_root: Path, kind: str, artifact: Mapping[str, Any]) -> Path:
    if kind == "asset-spec-2d":
        return work_root / "asset-specs" / f"{artifact['asset_id']}.json"
    if kind == "godot-binding":
        return work_root / "godot-bindings" / f"{artifact['binding_id']}.json"
    try:
        return work_root / ARTIFACT_PATHS[kind]
    except KeyError as exc:
        raise KeyError(f"Artifact kind cannot be recorded: {kind}") from exc


def rebuild_index(project_root: Path) -> dict[str, Any]:
    record_root = project_root / ".vibegame" / "gamemaker"
    works: list[dict[str, Any]] = []
    work_parent = record_root / "work"
    if work_parent.is_dir():
        for work_root in sorted(path for path in work_parent.iterdir() if path.is_dir()):
            card = work_root / "production-card.json"
            if not card.is_file():
                continue
            implementation = work_root / "implementation.json"
            evidence = work_root / "evidence" / "evidence-bundle.json"
            status = "implemented" if implementation.is_file() else "specified"
            entry: dict[str, Any] = {
                "work_id": work_root.name,
                "path": work_root.relative_to(project_root).as_posix(),
                "production_card": card.relative_to(project_root).as_posix(),
                "status": status,
                "record_files": {
                    p.relative_to(project_root).as_posix():
                    hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(work_root.rglob('*'))
                    if p.is_file() and p.suffix in {'.json', '.md'}
                },
                "updated_at": datetime.now(UTC).isoformat(),
            }
            if evidence.is_file():
                review = review_work(project_root, work_root.name)
                verdict = review.get("verdict", "insufficient_evidence")
                entry["verdict"] = verdict
                entry["status"] = {
                    "pass": "verified",
                    "fail": "failed",
                    "insufficient_evidence": "insufficient_evidence",
                }[verdict]
            works.append(entry)
    index = {
        "schema_version": "0.1",
        "project_revision": project_revision(project_root),
        "source_files": source_manifest(project_root),
        "works": works,
    }
    issues = SchemaCatalog().validate("work-index", index)
    if issues:
        raise ValueError(f"Generated work index is invalid: {issues[0].path} {issues[0].message}")
    _write_json(record_root / "index.json", index)
    return index


def record_artifact(
    project_root: Path, work_id: str, kind: str, artifact: Mapping[str, Any]
) -> Path:
    if not SAFE_ID.fullmatch(work_id):
        raise ValueError(
            "work_id must contain only letters, digits, dots, underscores, and hyphens"
        )
    issues = SchemaCatalog().validate(kind, artifact)
    if issues:
        issue = issues[0]
        raise ValueError(f"Invalid {kind} at {issue.path}: {issue.message}")
    work_root = project_root.resolve() / ".vibegame" / "gamemaker" / "work" / work_id
    path = _artifact_path(work_root, kind, artifact)
    if not path.resolve().is_relative_to(work_root):
        raise ValueError('Artifact path escapes work directory')
    _write_json(path, artifact)
    if kind == 'decision-card':
        (work_root / 'decision.md').write_text(
            '# Confirmed decision\n\n' + artifact['decision'] + '\n', encoding='utf-8'
        )
    rebuild_index(project_root.resolve())
    return path

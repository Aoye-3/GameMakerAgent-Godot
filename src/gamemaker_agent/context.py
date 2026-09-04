"""Compile audience-specific context from confirmed project records."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> Any | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_directory(path: Path) -> list[Any]:
    if not path.is_dir():
        return []
    return [_read_json(item) for item in sorted(path.glob("*.json"))]


def build_context_pack(project_root: Path, work_id: str, audience: str) -> dict[str, Any]:
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', work_id):
        raise ValueError('Invalid work_id')
    work = project_root.resolve() / ".vibegame" / "gamemaker" / "work" / work_id
    if not work.is_dir():
        raise FileNotFoundError(f"Unknown GameMaker work: {work_id}")
    if audience not in {"asset-provider", "programmer", "reviewer"}:
        raise ValueError(f"Unknown context audience: {audience}")

    decision = work / "decision.md"
    confirmed = _read_json(work / 'decision-card.json')
    common = {
        "schema_version": "0.1",
        "work_id": work_id,
        "audience": audience,
        "decision": confirmed,
        "decision_summary": (confirmed['decision'] if confirmed else
                             decision.read_text('utf-8') if decision.is_file() else None),
        "production_card": _read_json(work / "production-card.json"),
    }
    if audience == "asset-provider":
        return {"schema_version": "0.1", "work_id": work_id, "audience": audience,
                "asset_specs": _read_json_directory(work / "asset-specs")}
    elif audience == "programmer":
        common.update(
            {
                "project_context": _read_json(work / "project-context.json"),
                "normalized_assets": _read_json(work / "normalized-assets.json"),
                "godot_bindings": _read_json_directory(work / "godot-bindings"),
            }
        )
    else:
        common.pop('decision')
        common.pop('decision_summary')
        common['acceptance'] = (common.pop('production_card') or {}).get('acceptance', [])
        common.update(
            {
                "implementation": _read_json(work / "implementation.json"),
                "evidence": _read_json_directory(work / "evidence"),
            }
        )
    return common

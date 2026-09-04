"""Load and validate the public JSON contracts.

The JSON Schema files are the canonical model.  This module deliberately returns
plain dictionaries and validation issues instead of duplicating them as Python
domain classes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_FILES = {
    "asset-spec-2d": "asset-spec-2d.schema.json",
    "decision-card": "decision-card.schema.json",
    "evidence-bundle": "evidence-bundle.schema.json",
    "godot-binding": "godot-binding.schema.json",
    "implementation-record": "implementation-record.schema.json",
    "normalized-assets": "normalized-assets.schema.json",
    "production-card": "production-card.schema.json",
    "project-context": "project-context.schema.json",
    "provider-capability-profile": "provider-capability-profile.schema.json",
    "work-index": "work-index.schema.json",
}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    validator: str


def _default_schema_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "schemas"
        if (candidate / "evidence-bundle.schema.json").is_file():
            return candidate
    raise FileNotFoundError("Could not locate the GameMakerAgent schemas directory")


class SchemaCatalog:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or _default_schema_root()).resolve()

    @property
    def kinds(self) -> tuple[str, ...]:
        return tuple(sorted(SCHEMA_FILES))

    def load(self, kind: str) -> dict[str, Any]:
        try:
            filename = SCHEMA_FILES[kind]
        except KeyError as exc:
            raise KeyError(f"Unknown artifact kind: {kind}") from exc
        with (self.root / filename).open(encoding="utf-8") as handle:
            return json.load(handle)

    def check_all(self) -> None:
        for kind in self.kinds:
            Draft202012Validator.check_schema(self.load(kind))

    def validate(self, kind: str, instance: Mapping[str, Any]) -> list[ValidationIssue]:
        validator = Draft202012Validator(
            self.load(kind), format_checker=FormatChecker()
        )
        issues: list[ValidationIssue] = []
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            suffix = "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path
            )
            issues.append(
                ValidationIssue(
                    path=f"${suffix}",
                    message=error.message,
                    validator=str(error.validator),
                )
            )
        return issues

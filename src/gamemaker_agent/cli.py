"""Command-line interface for deterministic GameMaker context operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .context import build_context_pack
from .delivery import review_delivery
from .doctor import diagnose
from .project import query_project
from .providers import FakeProvider
from .records import record_artifact
from .schemas import SchemaCatalog


def _read(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gamemaker")
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor")
    doctor.add_argument("--project", type=Path, default=Path.cwd())
    doctor.add_argument("--godot", type=Path)
    query = commands.add_parser("query")
    query.add_argument("--project", type=Path, default=Path.cwd())
    query.add_argument("--term", action="append", default=[])
    validate = commands.add_parser("validate")
    validate.add_argument("--kind", required=True, choices=SchemaCatalog().kinds)
    validate.add_argument("--input", required=True)
    record = commands.add_parser("record")
    record.add_argument("--project", type=Path, default=Path.cwd())
    record.add_argument("--work", required=True)
    record.add_argument("--kind", required=True, choices=SchemaCatalog().kinds)
    record.add_argument("--input", required=True)
    context = commands.add_parser("context")
    context.add_argument("--project", type=Path, default=Path.cwd())
    context.add_argument("--work", required=True)
    context.add_argument(
        "--audience", required=True, choices=["asset-provider", "programmer", "reviewer"]
    )
    rehearse = commands.add_parser("rehearse")
    rehearse.add_argument("--capability", required=True)
    rehearse.add_argument("--advertise", action="append", default=[])
    profile = commands.add_parser("provider")
    profile_commands = profile.add_subparsers(dest="provider_command", required=True)
    check = profile_commands.add_parser("check")
    check.add_argument("--profile", required=True)
    check.add_argument("--require", action="append", default=[])
    evidence = commands.add_parser("evidence")
    evidence_commands = evidence.add_subparsers(dest="evidence_command", required=True)
    review = evidence_commands.add_parser("review")
    review.add_argument("--input", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "doctor":
        result = diagnose(args.project, args.godot)
        _print(result)
        return 0 if result["ready"] else 1
    if args.command == "query":
        _print(query_project(args.project, args.term))
        return 0
    if args.command == "validate":
        issues = SchemaCatalog().validate(args.kind, _read(args.input))
        _print({"valid": not issues, "issues": [vars(item) for item in issues]})
        return 0 if not issues else 1
    if args.command == "record":
        path = record_artifact(args.project, args.work, args.kind, _read(args.input))
        _print({"recorded": str(path)})
        return 0
    if args.command == "context":
        _print(build_context_pack(args.project, args.work, args.audience))
        return 0
    if args.command == "rehearse":
        result = FakeProvider("rehearsal", set(args.advertise)).invoke(args.capability, {})
        _print(result)
        return 0 if result["ok"] else 1
    if args.command == "provider":
        profile = _read(args.profile)
        issues = SchemaCatalog().validate("provider-capability-profile", profile)
        missing = sorted(set(args.require) - set(profile.get("capabilities", [])))
        _print({"valid": not issues, "missing": missing, "issues": [vars(item) for item in issues]})
        return 0 if not issues and not missing else 1
    request = _read(args.input)
    result = review_delivery(**request)
    _print(result)
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

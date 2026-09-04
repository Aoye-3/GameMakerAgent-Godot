import json
from pathlib import Path

from gamemaker_agent.cli import main


def test_query_cli_prints_machine_readable_project_context(tmp_path: Path, capsys) -> None:
    (tmp_path / "project.godot").write_text(
        '[application]\nrun/main_scene="res://main.tscn"\n', encoding="utf-8"
    )

    exit_code = main(["query", "--project", str(tmp_path), "--term", "player"])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["project_state"] == "godot_project"


def test_doctor_is_read_only_and_reports_missing_environment(tmp_path: Path, capsys) -> None:
    exit_code = main(["doctor", "--project", str(tmp_path)])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert not (tmp_path / ".vibegame").exists()
    assert any(check["name"] == "godot_project" and not check["ok"] for check in output["checks"])


def test_validate_cli_returns_nonzero_with_field_paths(tmp_path: Path, capsys) -> None:
    artifact = tmp_path / "card.json"
    artifact.write_text('{"schema_version":"0.1"}', encoding="utf-8")

    exit_code = main(
        ["validate", "--kind", "production-card", "--input", str(artifact)]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert output["issues"][0]["path"].startswith("$")


def test_doctor_checks_dock_in_target_project_not_framework(tmp_path: Path, capsys) -> None:
    (tmp_path / "project.godot").write_text('[application]\n', encoding="utf-8")

    assert main(["doctor", "--project", str(tmp_path)]) == 1

    output = json.loads(capsys.readouterr().out)
    dock = next(check for check in output["checks"] if check["name"] == "godot_dock")
    assert not dock["ok"]

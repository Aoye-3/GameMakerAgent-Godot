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


def test_live_doctor_cannot_confuse_connection_with_conformance(tmp_path, monkeypatch) -> None:
    from gamemaker_agent import doctor

    monkeypatch.setattr(doctor, 'live_probe', lambda *_: {'connected': True})
    report = doctor.diagnose(tmp_path, live=True)
    assert report['provider_connected']
    assert report['conformance_passed'] is None
    assert not report['ready']


def test_conformance_requires_intact_run_artifacts(tmp_path) -> None:
    import hashlib

    from gamemaker_agent.doctor import conformance_record_valid

    root = tmp_path / '.vibegame/gamemaker'
    root.mkdir(parents=True)
    trace = root / 'trace.json'
    trace.write_text('{}')
    record = {
        'project': str(tmp_path), 'provider_version': '3.2.4', 'reconnected': True,
        'rounds': [{'passed': True, 'run_id': str(i), 'artifacts': [{
            'path': '.vibegame/gamemaker/trace.json',
            'sha256': hashlib.sha256(trace.read_bytes()).hexdigest(),
        }]} for i in (1, 2)],
    }
    (root / 'conformance.json').write_text(json.dumps(record))
    probe = {'session': {'plugin_version': '3.2.4'}}
    assert conformance_record_valid(tmp_path, probe)
    trace.write_text('{"changed":true}')
    assert not conformance_record_valid(tmp_path, probe)


def test_context_cli_uses_utf8_even_with_legacy_stdout(tmp_path) -> None:
    import os
    import subprocess
    import sys

    project = tmp_path / '中文项目'
    project.mkdir()
    (project / 'project.godot').write_text('[application]\n', encoding='utf-8')
    result = subprocess.run(
        [sys.executable, '-m', 'gamemaker_agent.cli', 'query', '--project', str(project)],
        capture_output=True, env={**os.environ, 'PYTHONIOENCODING': 'ascii'}, check=True,
    )
    assert json.loads(result.stdout.decode('utf-8'))['project_root'] == str(project)

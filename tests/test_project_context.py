from pathlib import Path

from gamemaker_agent.project import is_context_stale, query_project


def _write_project(root: Path) -> None:
    (root / "scenes").mkdir()
    (root / "scripts").mkdir()
    (root / "project.godot").write_text(
        '[application]\nconfig/features=PackedStringArray("4.7", "GL Compatibility")\n'
        'run/main_scene="res://scenes/main.tscn"\n\n'
        '[input/move_left]\ndeadzone=0.5\n\n[input/collect]\ndeadzone=0.5\n',
        encoding="utf-8",
    )
    (root / "scenes" / "main.tscn").write_text(
        '[gd_scene]\n[node name="Player" type="CharacterBody2D"]\n', encoding="utf-8"
    )
    (root / "scripts" / "inventory.gd").write_text(
        "var items_collected := 0\n", encoding="utf-8"
    )
    (root / "scripts" / "unrelated.gd").write_text(
        "var weather := 'sunny'\n", encoding="utf-8"
    )


def test_query_returns_bounded_task_relevant_godot_facts(tmp_path: Path) -> None:
    _write_project(tmp_path)

    result = query_project(tmp_path, terms=["player", "collect"])

    assert result["project_state"] == "godot_project"
    assert result["engine"]["main_scene"] == "res://scenes/main.tscn"
    assert result["engine"]["input_actions"] == ["collect", "move_left"]
    assert {fact["source"] for fact in result["facts"]} == {
        "project.godot",
        "scenes/main.tscn",
        "scripts/inventory.gd",
    }
    assert len(result["facts"]) <= 20


def test_context_becomes_stale_when_project_source_changes(tmp_path: Path) -> None:
    _write_project(tmp_path)
    result = query_project(tmp_path, terms=["collect"])

    assert not is_context_stale(result, tmp_path)
    (tmp_path / "scripts" / "inventory.gd").write_text(
        "var items_collected := 1\n", encoding="utf-8"
    )

    assert is_context_stale(result, tmp_path)


def test_non_godot_workspace_is_reported_without_fabricated_facts(tmp_path: Path) -> None:
    result = query_project(tmp_path, terms=[])

    assert result["project_state"] == "non_godot"
    assert result["facts"] == []

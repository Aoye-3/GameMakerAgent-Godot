from pathlib import Path

from gamemaker_agent.project import is_context_stale, query_project


def _write_project(root: Path) -> None:
    (root / "scenes").mkdir()
    (root / "scripts").mkdir()
    (root / "project.godot").write_text(
        '[application]\nconfig/features=PackedStringArray("4.7", "GL Compatibility")\n'
        'run/main_scene="res://scenes/main.tscn"\n\n'
        '[input]\nmove_left={\n"deadzone": 0.5,\n"events": []\n}\n'
        'collect={\n"deadzone": 0.5,\n"events": []\n}\n',
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


def test_uid_entry_resolves_without_import_cache(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "project.godot").write_text(
        '[application]\nrun/main_scene="uid://abc"\n', encoding="utf-8"
    )
    (tmp_path / "scenes/main.tscn").write_text(
        '[gd_scene format=3 uid="uid://abc"]\n', encoding="utf-8"
    )
    assert query_project(tmp_path, [])['engine']['main_scene'] == 'res://scenes/main.tscn'


def test_fingerprint_covers_asset_and_import_but_excludes_external_addons(tmp_path: Path) -> None:
    _write_project(tmp_path)
    png = tmp_path / "player.png"
    png.write_bytes(b"first asset")
    before = query_project(tmp_path, [])
    png.write_bytes(b"replacement asset")
    assert is_context_stale(before, tmp_path)
    before = query_project(tmp_path, [])
    (tmp_path / "player.png.import").write_text('[params]\nfilter=false\n')
    assert is_context_stale(before, tmp_path)
    before = query_project(tmp_path, [])
    addon = tmp_path / "addons/godot_ai"
    addon.mkdir(parents=True)
    (addon / "plugin.gd").write_text("extends EditorPlugin\n")
    assert not is_context_stale(before, tmp_path)
    assert not any('godot_ai' in fact['source'] for fact in query_project(tmp_path, [])['facts'])

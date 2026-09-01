import json

from gamemaker_agent.doctor import diagnose, repository_root
from gamemaker_agent.schemas import SchemaCatalog


def test_repo_plugin_marketplace_and_skills_form_one_installable_package() -> None:
    root = repository_root()
    plugin_root = root / "plugins/gamemaker-agent"
    manifest = json.loads((plugin_root / ".codex-plugin/plugin.json").read_text("utf-8"))
    marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text("utf-8"))

    assert manifest["name"] == "gamemaker-agent"
    assert manifest["skills"] == "./skills/"
    assert "mcpServers" not in manifest
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/gamemaker-agent"
    for name in ("studio-advisor", "game-delivery", "evidence-review"):
        text = (plugin_root / "skills" / name / "SKILL.md").read_text("utf-8")
        assert "[TODO:" not in text


def test_provider_profiles_validate_against_public_schema() -> None:
    root = repository_root()
    profile = json.loads(
        (root / "adapters/profiles/godot-ai-3.2.4.json").read_text("utf-8")
    )

    assert SchemaCatalog().validate("provider-capability-profile", profile) == []
    assert "step_until" not in profile["capabilities"]


def test_dock_source_contains_no_write_or_runtime_control_operations() -> None:
    source = (
        repository_root() / "godot/addons/gamemaker_context/read_only_dock.gd"
    ).read_text("utf-8")

    forbidden_operations = (
        "FileAccess.WRITE",
        "store_",
        "DirAccess",
        "play_main_scene",
        "stop_playing_scene",
    )
    for forbidden in forbidden_operations:
        assert forbidden not in source


def test_doctor_recognizes_the_packaged_fixture_environment() -> None:
    root = repository_root()

    report = diagnose(root / "godot")

    assert report["ready"], report

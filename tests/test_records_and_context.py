import json
from pathlib import Path

from gamemaker_agent.context import build_context_pack
from gamemaker_agent.records import record_artifact


def test_record_validates_writes_and_rebuilds_work_index(tmp_path: Path) -> None:
    card = {
        "schema_version": "0.1",
        "production_id": "collect-coin",
        "project_context_id": "ctx-1",
        "player_outcome": "The player understands that touching the target collects it.",
        "beat": "Move, touch, receive immediate feedback.",
        "reuse": ["res://scenes/main.tscn"],
        "new_assets": ["player-sprite"],
        "acceptance": ["items_collected changes from 0 to 1"],
    }

    path = record_artifact(tmp_path, "collect-coin", "production-card", card)

    assert path == tmp_path / ".vibegame/gamemaker/work/collect-coin/production-card.json"
    index = json.loads((tmp_path / ".vibegame/gamemaker/index.json").read_text("utf-8"))
    assert index["works"][0]["work_id"] == "collect-coin"
    assert index["works"][0]["status"] == "specified"


def test_context_pack_contains_confirmed_artifacts_not_chat_transcript(tmp_path: Path) -> None:
    work = tmp_path / ".vibegame/gamemaker/work/collect-coin"
    work.mkdir(parents=True)
    (work / "decision.md").write_text(
        "# Confirmed decision\nUse a readable silhouette.\n", encoding="utf-8"
    )
    (work / "chat-transcript.md").write_text("private brainstorming", encoding="utf-8")
    (work / "production-card.json").write_text(
        json.dumps({"production_id": "collect-coin", "acceptance": ["count becomes 1"]}),
        encoding="utf-8",
    )
    (work / "project-context.json").write_text(
        json.dumps({"context_id": "ctx-1", "facts": [{"kind": "scene"}]}),
        encoding="utf-8",
    )

    pack = build_context_pack(tmp_path, "collect-coin", audience="programmer")

    assert pack["decision_summary"].startswith("# Confirmed decision")
    assert pack["production_card"]["production_id"] == "collect-coin"
    assert "private brainstorming" not in json.dumps(pack)

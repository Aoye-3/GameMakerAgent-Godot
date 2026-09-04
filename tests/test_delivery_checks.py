from pathlib import Path

from PIL import Image

from gamemaker_agent.assets import inspect_asset, normalize_asset
from gamemaker_agent.delivery import review_delivery
from gamemaker_agent.providers import FakeProvider


def _asset_spec() -> dict:
    return {
        "schema_version": "0.1",
        "asset_id": "player-sprite",
        "production_id": "collect-coin",
        "role": "Readable player avatar",
        "visual": {"style": "flat silhouette", "player_read": "player-controlled character"},
        "technical": {
            "format": "png", "width": 64, "height": 64, "frames": 1,
            "transparent": True, "pivot": {"x": 0.5, "y": 0.5}, "trim": False
        },
        "provenance": {"source_kind": "fixture", "license": "CC0-1.0"},
        "normalization": {"target_path": "res://assets/player.png", "artifact_id": "player-r1"},
    }


def test_asset_inspector_accepts_matching_rgba_png(tmp_path: Path) -> None:
    image_path = tmp_path / "player.png"
    picture = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    picture.putpixel((32, 32), (255, 255, 255, 255))
    picture.save(image_path)

    report = inspect_asset(_asset_spec(), image_path)

    assert report["accepted"]
    assert report["issues"] == []


def test_asset_inspector_blocks_wrong_dimensions_and_missing_alpha(tmp_path: Path) -> None:
    image_path = tmp_path / "player.png"
    Image.new("RGB", (32, 64), (255, 255, 255)).save(image_path)

    report = inspect_asset(_asset_spec(), image_path)

    assert not report["accepted"]
    assert {issue["code"] for issue in report["issues"]} == {"dimensions", "transparency"}


def test_delivery_review_rejects_unbound_assets_and_stale_evidence() -> None:
    result = review_delivery(
        production={"production_id": "collect-coin", "new_assets": ["player-sprite"]},
        asset_specs=[_asset_spec()],
        bindings=[],
        normalized_assets=[{"asset_id": "player-sprite", "artifact_id": "player-r1"}],
        implementation={
            "implementation_id": "impl-1", "production_id": "collect-coin",
            "source_revision": "rev-2", "binding_ids": []
        },
        evidence={
            "implementation": {"implementation_id": "impl-1", "source_revision": "rev-1"},
            "assertions": [{"passed": True}], "diagnostics": {"errors": []}
        },
    )

    assert result["verdict"] == "insufficient_evidence"
    assert {"unbound_asset", "stale_evidence"} <= {issue["code"] for issue in result["issues"]}


def test_fake_provider_reports_unsupported_capability_without_simulating_it() -> None:
    provider = FakeProvider("runtime-fixture", {"start", "input", "observe"})

    result = provider.invoke("step_until", {"predicate": "items_collected == 1"})

    assert not result["ok"]
    assert result["error"]["category"] == "unsupported_capability"


def test_blank_and_opaque_rgba_are_not_usable_transparent_sprites(tmp_path: Path) -> None:
    path = tmp_path / 'sprite.png'
    for alpha in (0, 255):
        Image.new('RGBA', (64, 64), (255, 255, 255, alpha)).save(path)
        assert not inspect_asset(_asset_spec(), path)['accepted']


def test_normalization_keeps_source_hash_and_stable_target(tmp_path: Path) -> None:
    source = tmp_path / 'source.png'
    picture = Image.new('RGBA', (128, 128))
    picture.paste((50, 200, 200, 255), (32, 32, 96, 96))
    picture.save(source)
    record = normalize_asset(_asset_spec(), source, tmp_path)
    assert record['path'] == 'res://assets/player.png'
    assert record['asset_id'] == 'player-sprite'
    assert len(record['sha256']) == 64
    assert inspect_asset(_asset_spec(), tmp_path / 'assets/player.png')['accepted']

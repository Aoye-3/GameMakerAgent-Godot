import json

from gamemaker_agent.doctor import repository_root


def test_skill_routing_cases_cover_positive_and_negative_boundaries() -> None:
    cases = json.loads((repository_root() / "evals/routing-cases.json").read_text("utf-8"))["cases"]
    expected = {case["expected_skill"] for case in cases}

    assert expected == {None, "studio-advisor", "game-delivery", "evidence-review"}
    assert len({case["id"] for case in cases}) == len(cases)


def test_godot_ai_profile_satisfies_required_conformance_capabilities() -> None:
    root = repository_root()
    matrix = json.loads((root / "evals/provider-conformance.json").read_text("utf-8"))
    profile = json.loads((root / "adapters/profiles/godot-ai-3.2.4.json").read_text("utf-8"))

    assert set(matrix["required"]) <= set(profile["capabilities"])
    assert set(matrix["optional_with_explicit_degradation"]).isdisjoint(profile["capabilities"])

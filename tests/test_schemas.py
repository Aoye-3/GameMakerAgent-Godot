from gamemaker_agent.schemas import SchemaCatalog


def test_all_public_schemas_are_discoverable_and_valid() -> None:
    catalog = SchemaCatalog()

    assert set(catalog.kinds) == {
        "asset-spec-2d",
        "decision-card",
        "evidence-bundle",
        "godot-binding",
        "implementation-record",
        "production-card",
        "project-context",
        "provider-capability-profile",
        "work-index",
    }
    catalog.check_all()


def test_validation_reports_a_stable_json_path() -> None:
    errors = SchemaCatalog().validate(
        "production-card",
        {"schema_version": "0.1", "production_id": "work-1"},
    )

    assert errors
    assert errors[0].path.startswith("$")
    assert errors[0].message

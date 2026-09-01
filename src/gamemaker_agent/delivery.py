"""Cross-artifact invariants for a completed delivery."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def review_delivery(
    *,
    production: Mapping[str, Any],
    asset_specs: Sequence[Mapping[str, Any]],
    bindings: Sequence[Mapping[str, Any]],
    normalized_assets: Sequence[Mapping[str, Any]],
    implementation: Mapping[str, Any] | None,
    evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    spec_ids = {item.get("asset_id") for item in asset_specs}
    bound_ids = {item.get("asset_id") for item in bindings}
    normalized = {
        (item.get("asset_id"), item.get("artifact_id")) for item in normalized_assets
    }
    for asset_id in production.get("new_assets", []):
        if asset_id not in spec_ids:
            issues.append({"code": "missing_asset_spec", "message": str(asset_id)})
        elif asset_id not in bound_ids:
            issues.append({"code": "unbound_asset", "message": str(asset_id)})
    for binding in bindings:
        pair = (binding.get("asset_id"), binding.get("artifact_id"))
        if pair not in normalized:
            issues.append({"code": "missing_normalized_asset", "message": str(pair)})
    if implementation is None or evidence is None:
        issues.append(
            {"code": "missing_evidence", "message": "Implementation and evidence are required"}
        )
    else:
        evidence_impl = evidence.get("implementation", {})
        if (
            evidence_impl.get("implementation_id") != implementation.get("implementation_id")
            or evidence_impl.get("source_revision") != implementation.get("source_revision")
        ):
            issues.append(
                {"code": "stale_evidence", "message": "Evidence does not match implementation"}
            )
        failed = [item for item in evidence.get("assertions", []) if not item.get("passed")]
        errors = evidence.get("diagnostics", {}).get("errors", [])
        if failed or errors:
            issues.append(
                {"code": "runtime_failure", "message": "Assertions or diagnostics failed"}
            )
    codes = {issue["code"] for issue in issues}
    verdict = "pass"
    if "runtime_failure" in codes:
        verdict = "fail"
    elif issues:
        verdict = "insufficient_evidence"
    return {"verdict": verdict, "issues": issues}

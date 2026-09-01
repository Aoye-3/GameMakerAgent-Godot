"""Deterministic checks for V1 2D PNG assets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from PIL import Image

from .schemas import SchemaCatalog


def inspect_asset(spec: Mapping[str, Any], path: Path) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    for issue in SchemaCatalog().validate("asset-spec-2d", spec):
        issues.append(
            {"severity": "blocking", "code": "schema", "message": f"{issue.path}: {issue.message}"}
        )
    if not path.is_file():
        issues.append({"severity": "blocking", "code": "missing_file", "message": str(path)})
        return {"accepted": False, "asset_id": spec.get("asset_id"), "issues": issues}
    try:
        with Image.open(path) as image:
            technical = spec.get("technical", {})
            expected_size = (technical.get("width"), technical.get("height"))
            if image.format != "PNG":
                issues.append({"severity": "blocking", "code": "format", "message": "Expected PNG"})
            if image.size != expected_size:
                issues.append(
                    {
                        "severity": "blocking", "code": "dimensions",
                        "message": f"Expected {expected_size}, received {image.size}",
                    }
                )
            if technical.get("transparent") and "A" not in image.getbands():
                issues.append(
                    {
                        "severity": "blocking",
                        "code": "transparency",
                        "message": "Alpha channel required",
                    }
                )
    except OSError as exc:
        issues.append({"severity": "blocking", "code": "decode", "message": str(exc)})
    return {
        "accepted": not any(issue["severity"] == "blocking" for issue in issues),
        "asset_id": spec.get("asset_id"),
        "issues": issues,
    }

"""Deterministic checks for V1 2D PNG assets."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from PIL import Image, ImageOps

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
            elif technical.get("transparent"):
                low, high = image.getchannel('A').getextrema()
                if low == 255 or high == 0:
                    issues.append({
                        'severity': 'blocking', 'code': 'alpha_content',
                        'message': 'Sprite needs both visible content and transparent pixels',
                    })
    except OSError as exc:
        issues.append({"severity": "blocking", "code": "decode", "message": str(exc)})
    return {
        "accepted": not any(issue["severity"] == "blocking" for issue in issues),
        "asset_id": spec.get("asset_id"),
        "issues": issues,
    }


def normalize_asset(spec: Mapping[str, Any], source: Path, project: Path) -> dict[str, Any]:
    """Fit a single-frame PNG to the specified canvas; never remove its background."""
    issues = SchemaCatalog().validate('asset-spec-2d', spec)
    if issues:
        raise ValueError(f'Invalid asset specification: {issues}')
    technical = spec['technical']
    if technical['frames'] != 1 or technical['trim']:
        raise ValueError('Trial normalizer supports single-frame, untrimmed sprites only')
    root = project.resolve()
    target = (root / spec['normalization']['target_path'].removeprefix('res://')).resolve()
    if not target.is_relative_to(root) or target.suffix.lower() != '.png':
        raise ValueError('Asset target must be a PNG inside the project')
    with Image.open(source) as raw:
        raw_spec = dict(spec, technical=dict(technical, width=raw.width, height=raw.height))
        report = inspect_asset(raw_spec, source)
        if not report['accepted']:
            raise ValueError(f'Unusable raw asset: {report["issues"]}')
        size = (technical['width'], technical['height'])
        fitted = ImageOps.contain(raw.convert('RGBA'), size, Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', size)
        canvas.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.normalizing.png')
        canvas.save(temporary, format='PNG')
    report = inspect_asset(spec, temporary)
    if not report['accepted']:
        temporary.unlink()
        raise ValueError(f'Normalization failed validation: {report["issues"]}')
    temporary.replace(target)
    return {
        'asset_id': spec['asset_id'], 'artifact_id': spec['normalization']['artifact_id'],
        'path': spec['normalization']['target_path'],
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'source_path': source.resolve().relative_to(root).as_posix(),
        'provenance': spec['provenance'],
        'operations': ['RGBA conversion', 'Lanczos contain', 'transparent canvas padding'],
    }

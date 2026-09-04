"""Cross-artifact invariants for a completed delivery."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from .assets import inspect_asset
from .project import project_revision
from .schemas import SchemaCatalog


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
        if not evidence.get('assertions') or not evidence.get('artifacts'):
            issues.append({
                'code': 'missing_evidence', 'message': 'Assertions and artifacts required'
            })
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


def review_work(project: Path, work_id: str) -> dict[str, Any]:
    """Review stored artifacts against current native files, not a saved PASS label."""
    root = project.resolve()
    work = (root / '.vibegame/gamemaker/work' / work_id).resolve()
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]*', work_id):
        raise ValueError('Invalid work_id')
    issues: list[dict[str, str]] = []
    catalog = SchemaCatalog()

    def issue(code: str, message: str) -> None:
        issues.append({'code': code, 'message': message})

    def read(name: str, kind: str) -> dict:
        try:
            value = json.loads((work / name).read_text('utf-8'))
            errors = catalog.validate(kind, value)
            for error in errors:
                issue('schema', f'{name}{error.path}: {error.message}')
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError) as exc:
            issue('missing_record', f'{name}: {exc}')
            return {}

    def local(path: str) -> Path:
        result = (root / path.removeprefix('res://')).resolve()
        if not result.is_relative_to(root):
            raise ValueError(f'Path escapes project: {path}')
        return result

    production = read('production-card.json', 'production-card')
    implementation = read('implementation.json', 'implementation-record')
    evidence = read('evidence/evidence-bundle.json', 'evidence-bundle')
    normalized = read('normalized-assets.json', 'normalized-assets')
    context = read('project-context.json', 'project-context')
    if context.get('context_id') != production.get('project_context_id'):
        issue('context_mismatch', 'Production must reference its project context')
    if production.get('decision_id'):
        decision = read('decision-card.json', 'decision-card')
        if decision.get('decision_id') != production['decision_id']:
            issue('decision_mismatch', 'Production must reference its confirmed decision')
    specs = [read('asset-specs/' + p.name, 'asset-spec-2d')
             for p in sorted((work / 'asset-specs').glob('*.json'))]
    bindings = [read('godot-bindings/' + p.name, 'godot-binding')
                for p in sorted((work / 'godot-bindings').glob('*.json'))]
    if issues:
        return {'verdict': 'insufficient_evidence', 'issues': issues}
    result = review_delivery(
        production=production, asset_specs=specs, bindings=bindings,
        normalized_assets=normalized['assets'], implementation=implementation, evidence=evidence,
    )
    issues.extend(result['issues'])
    current = project_revision(root)
    if implementation['source_revision'] != current or evidence['source']['revision'] != current:
        issue('stale_evidence', 'Current native content no longer matches the recorded revision')
    production_id = production['production_id']
    if implementation['production_id'] != production_id:
        issue('production_mismatch', 'Implementation references a different production card')
    if set(implementation['binding_ids']) != {b['binding_id'] for b in bindings}:
        issue('binding_mismatch', 'Implementation binding references do not close')
    descriptions = {a['description'] for a in evidence['assertions']}
    if not set(production['acceptance']) <= descriptions:
        issue('missing_assertion', 'Not every acceptance claim has an assertion')
    if not any(a['kind'] == 'screenshot' for a in evidence['artifacts']):
        issue('missing_screenshot', 'Runtime screenshot required')
    try:
        for artifact in evidence['artifacts']:
            path = local(artifact['path'])
            if (not path.is_file()
                    or hashlib.sha256(path.read_bytes()).hexdigest() != artifact['sha256']):
                issue('artifact_integrity', artifact['path'])
            if artifact.get('stale_frame'):
                issue('stale_evidence', 'Provider reported a stale screenshot')
        for path in implementation['files']:
            if not local(path).is_file():
                issue('missing_implementation_file', path)
        by_asset = {a['asset_id']: a for a in normalized['assets']}
        if set(by_asset) - {b['asset_id'] for b in bindings}:
            issue('unbound_asset', 'Every normalized asset must be bound')
        if len(by_asset) != len(normalized['assets']):
            issue('duplicate_asset_id', 'Normalized asset IDs must be unique')
        for spec in specs:
            asset = by_asset.get(spec['asset_id'])
            if not asset or spec['production_id'] != production_id:
                issue('asset_reference', spec['asset_id'])
                continue
            path = local(asset['path'])
            raw = local(asset['source_path'])
            if (not raw.is_file()
                    or hashlib.sha256(raw.read_bytes()).hexdigest() != asset['source_sha256']):
                issue('asset_source_integrity', asset['source_path'])
            if not inspect_asset(spec, path)['accepted']:
                issue('invalid_asset', asset['path'])
            elif hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
                issue('stale_asset', asset['path'])
        for binding in bindings:
            if binding['production_id'] != production_id:
                issue('production_mismatch', binding['binding_id'])
            asset = by_asset.get(binding['asset_id'], {})
            if asset.get('path') != binding['resource']['path']:
                issue('binding_resource_mismatch', binding['binding_id'])
            scene = local(binding['node']['scene']).read_text('utf-8-sig')
            nodes = list(re.finditer(r'^\[node ([^\n]+)\]\n([^\[]*)', scene, re.M))
            root_name = re.search(r'name="([^"]+)"', nodes[0][1])[1] if nodes else ''
            matched = False
            for node in nodes:
                fields = dict(re.findall(r'(\w+)="([^"]*)"', node[1]))
                parent = fields.get('parent', '').strip('.')
                node_path = '/' + '/'.join(filter(None, [root_name, parent, fields['name']]))
                if 'parent' not in fields:
                    node_path = '/' + root_name
                if (node_path == binding['node']['path']
                        and fields.get('type') == binding['node']['type']):
                    for ext in re.findall(r'^\[ext_resource ([^\n]+)\]', scene, re.M):
                        attrs = dict(re.findall(r'(\w+)="([^"]*)"', ext))
                        if attrs.get('path') == binding['resource']['path']:
                            prop = 'texture' if fields['type'] == 'Sprite2D' else 'sprite_frames'
                            matched = bool(re.search(
                                rf'^{prop}\s*=\s*ExtResource\("{re.escape(attrs["id"])}"\)',
                                node[2], re.M,
                            ))
            if not matched:
                issue('binding_node_mismatch', binding['node']['path'])
    except (OSError, ValueError) as exc:
        issue('project_reference', str(exc))
    verdict = 'fail' if any(i['code'] == 'runtime_failure' for i in issues) else (
        'insufficient_evidence' if issues else 'pass'
    )
    return {'verdict': verdict, 'issues': issues, 'source_revision': current}

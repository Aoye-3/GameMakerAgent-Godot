import copy
import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from gamemaker_agent.assets import normalize_asset
from gamemaker_agent.cli import main
from gamemaker_agent.delivery import review_work
from gamemaker_agent.project import project_revision, query_project
from gamemaker_agent.providers import FakeProvider
from gamemaker_agent.records import record_artifact


def test_old_or_empty_evidence_cannot_be_pass(tmp_path: Path) -> None:
    work = tmp_path / '.vibegame/gamemaker/work/trial'
    (work / 'evidence').mkdir(parents=True)
    (work / 'production-card.json').write_text(json.dumps({
        'production_id': 'trial', 'new_assets': [], 'acceptance': ['collect']
    }))
    (work / 'implementation.json').write_text(json.dumps({
        'implementation_id': 'impl', 'production_id': 'trial',
        'source_revision': project_revision(tmp_path), 'files': [], 'binding_ids': []
    }))
    (work / 'evidence/evidence-bundle.json').write_text(json.dumps({
        'review': {'verdict': 'pass'}, 'assertions': [], 'diagnostics': {'errors': []}
    }))
    assert review_work(tmp_path, 'trial')['verdict'] == 'insufficient_evidence'


def test_decision_json_is_the_context_truth(tmp_path: Path) -> None:
    from gamemaker_agent.context import build_context_pack

    decision = {
        'schema_version': '0.1', 'decision_id': 'd1', 'status': 'confirmed',
        'player_outcome': 'collect', 'decision': 'single scene',
        'constraints': [], 'source_revision': 'rev',
    }
    record_artifact(tmp_path, 'trial', 'decision-card', decision)
    pack = build_context_pack(tmp_path, 'trial', 'programmer')
    assert pack['decision']['decision_id'] == 'd1'
    assert (tmp_path / '.vibegame/gamemaker/work/trial/decision.md').exists()


def test_normalized_list_can_roundtrip_through_records(tmp_path: Path) -> None:
    digest = hashlib.sha256(b'asset').hexdigest()
    record = {
        'schema_version': '0.1', 'assets': [{
            'asset_id': 'player', 'artifact_id': 'player-r1', 'path': 'res://player.png',
            'sha256': digest, 'source_sha256': digest, 'source_path': 'raw.png',
            'provenance': {'source_kind': 'generated', 'license': 'internal'},
            'operations': ['contain'],
        }]
    }
    before = copy.deepcopy(record)
    path = record_artifact(tmp_path, 'trial', 'normalized-assets', record)
    assert path.name == 'normalized-assets.json'
    assert json.loads(path.read_text()) == before


def complete_work(root: Path, provider_id: str = 'fake-a') -> Path:
    from test_delivery_checks import _asset_spec

    (root / 'project.godot').write_text('[application]\nconfig/name="test"\n')
    (root / 'player.gd').write_text('extends Node2D\n')
    (root / 'main.tscn').write_text(
        '[gd_scene format=3]\n'
        '[ext_resource type="Texture2D" path="res://assets/player.png" id="1"]\n'
        '[node name="Main" type="Node2D"]\n'
        '[node name="Player" type="Sprite2D" parent="."]\ntexture = ExtResource("1")\n'
    )
    artifacts = root / '.vibegame/gamemaker/artifacts'
    artifacts.mkdir(parents=True)
    raw = artifacts / 'raw.png'
    picture = Image.new('RGBA', (64, 64))
    picture.paste((40, 180, 190, 255), (16, 16, 48, 48))
    picture.save(raw)
    picture.save(artifacts / 'screen.png')
    spec = _asset_spec()
    asset = normalize_asset(spec, raw, root)
    context = query_project(root, [])
    revision = context['source_revision']
    records = {
        'project-context': context,
        'production-card': {
            'schema_version': '0.1', 'production_id': 'collect-coin',
            'project_context_id': context['context_id'], 'player_outcome': 'collect',
            'beat': 'touch', 'reuse': [], 'new_assets': ['player-sprite'],
            'acceptance': ['collect'],
        },
        'asset-spec-2d': spec,
        'normalized-assets': {'schema_version': '0.1', 'assets': [asset]},
        'godot-binding': {
            'schema_version': '0.1', 'binding_id': 'b1', 'production_id': 'collect-coin',
            'asset_id': 'player-sprite', 'artifact_id': 'player-r1',
            'resource': {'path': asset['path'], 'type': 'Texture2D'},
            'node': {'scene': 'res://main.tscn', 'path': '/Main/Player', 'type': 'Sprite2D'},
            'import_options': {}, 'verification': ['visible'],
        },
        'implementation-record': {
            'schema_version': '0.1', 'implementation_id': 'impl',
            'production_id': 'collect-coin', 'source_revision': revision, 'summary': 'test',
            'files': ['res://main.tscn', 'res://player.gd'], 'binding_ids': ['b1'],
        },
        'evidence-bundle': {
            'schema_version': '0.1', 'evidence_id': 'e1',
            'implementation': {'implementation_id': 'impl', 'source_revision': revision},
            'runtime': {'provider_id': provider_id, 'version': 'test',
                        'session_id': 'fixture-session', 'run_id': 'fixture-run'},
            'source': {'repository': 'synthetic-fixture', 'revision': revision},
            'toolchain': {'framework': 'test', 'runtime_adapter': provider_id, 'engine': 'fake'},
            'scenario': {'id': 'collect', 'goal': 'collect'},
            'input_trace': [], 'observations': {'before': {'count': 0}, 'after': {'count': 1}},
            'assertions': [{'description': 'collect', 'passed': True}],
            'diagnostics': {'errors': [], 'warnings': []},
            'artifacts': [{'kind': 'screenshot',
                           'path': '.vibegame/gamemaker/artifacts/screen.png',
                           'sha256': hashlib.sha256(
                               (artifacts / 'screen.png').read_bytes()).hexdigest()}],
            'timing': {'started_at': '2026-09-04T00:00:00Z',
                       'finished_at': '2026-09-04T00:00:01Z'},
            'review': {'reviewer': 'test', 'verdict': 'pass'},
        },
    }
    for kind, value in records.items():
        # Exercise the CLI record path with the same schema used by real work.
        source = artifacts / f'{kind}.json'
        source.write_text(json.dumps(value), encoding='utf-8')
        assert main(['record', '--project', str(root), '--work', 'trial',
                     '--kind', kind, '--input', str(source)]) == 0
    return root / '.vibegame/gamemaker/work/trial'


@pytest.mark.parametrize('provider_id', ['fake-a', 'fake-b'])
@pytest.mark.parametrize('case', ['success', 'timeout', 'unsupported', 'runtime_failure',
                                 'invalid_asset', 'stale_script', 'stale_png',
                                 'missing_screenshot', 'wrong_node', 'missing_run'])
def test_two_provider_record_review_matrix(tmp_path: Path, provider_id: str, case: str) -> None:
    work = complete_work(tmp_path, provider_id)
    evidence_path = work / 'evidence/evidence-bundle.json'
    evidence = json.loads(evidence_path.read_text('utf-8'))
    assert main(['evidence', 'review', '--project', str(tmp_path), '--work', 'trial']) == 0
    if case in {'timeout', 'unsupported', 'runtime_failure'}:
        def handler(_request):
            if case == 'timeout':
                raise TimeoutError('timed out')
            raise RuntimeError('run failed')
        provider = FakeProvider(provider_id, set() if case == 'unsupported' else {'start'},
                                {'start': handler})
        result = provider.invoke('start', {})
        assert not result['ok']
        expected = {'timeout': 'timeout', 'unsupported': 'unsupported_capability',
                    'runtime_failure': 'execution_failed'}[case]
        assert result['error']['category'] == expected
        evidence['diagnostics']['errors'] = [result['error']]
    elif case == 'invalid_asset':
        Image.new('RGBA', (64, 64)).save(tmp_path / 'assets/player.png')
    elif case == 'stale_script':
        (tmp_path / 'player.gd').write_text('extends Node2D\n# changed\n')
    elif case == 'stale_png':
        picture = Image.open(tmp_path / 'assets/player.png').copy()
        picture.putpixel((32, 32), (255, 0, 0, 255))
        picture.save(tmp_path / 'assets/player.png')
    elif case == 'missing_screenshot':
        evidence['artifacts'] = []
    elif case == 'wrong_node':
        path = work / 'godot-bindings/b1.json'
        binding = json.loads(path.read_text())
        binding['node']['path'] = '/Main/NotPlayer'
        path.write_text(json.dumps(binding))
    elif case == 'missing_run':
        del evidence['runtime']['run_id']
    evidence_path.write_text(json.dumps(evidence))
    report = review_work(tmp_path, 'trial')
    assert (report['verdict'] == 'pass') == (case == 'success'), report
    assert main(['evidence', 'review', '--project', str(tmp_path), '--work', 'trial']) == (
        0 if case == 'success' else 1
    )

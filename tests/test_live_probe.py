import asyncio
import importlib.util
import sys
from types import SimpleNamespace

from gamemaker_agent.doctor import repository_root


def test_running_game_is_still_a_connected_provider(tmp_path, monkeypatch):
    class Client:
        def __init__(self, *_args, **_kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args):
            pass

        async def call_tool(self, name, arguments):
            if name == 'session_manage':
                assert arguments == {'op': 'list'}
                return SimpleNamespace(data={'sessions': [{
                    'project_path': str(tmp_path), 'session_id': 'trial', 'readiness': 'playing'
                }]})
            assert name == 'editor_state'
            assert arguments == {'session_id': 'trial'}
            return SimpleNamespace(data={'readiness': 'playing', 'is_playing': True})

    monkeypatch.setitem(sys.modules, 'fastmcp', SimpleNamespace(Client=Client))
    spec = importlib.util.spec_from_file_location(
        'trial_probe', repository_root() / 'adapters/godot-ai/probe.py'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = asyncio.run(module.probe(tmp_path))
    assert result['connected'] is True

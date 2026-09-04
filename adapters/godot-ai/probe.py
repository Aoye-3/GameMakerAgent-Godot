"""Read-only live probe; executed by the pinned provider's existing Python environment."""

import asyncio
import json
import sys
from pathlib import Path

from fastmcp import Client


async def probe(project: Path) -> dict:
    async with Client('http://127.0.0.1:8000/mcp', timeout=10) as client:
        sessions = (await client.call_tool('session_manage', {'op': 'list'})).data
        if not isinstance(sessions, dict):
            raise ValueError('Unexpected session response')
        matches = [s for s in sessions.get('sessions', [])
                   if Path(s['project_path']).resolve() == project.resolve()]
        if len(matches) != 1:
            return {'connected': False, 'error': 'Expected exactly one matching project session',
                    'matching_sessions': len(matches)}
        session = matches[0]
        state = (await client.call_tool('editor_state', {
            'session_id': session['session_id']
        })).data
        # A successful editor query proves connectivity, including while playing.
        return {'connected': True,
                'session': session, 'editor_state': state}


if __name__ == '__main__':
    try:
        result = asyncio.run(probe(Path(sys.argv[1])))
    except Exception as exc:
        result = {'connected': False, 'error': str(exc)}
    print(json.dumps(result))

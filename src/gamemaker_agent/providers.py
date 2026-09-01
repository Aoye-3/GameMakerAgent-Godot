"""Provider-neutral capability and error behavior used by contract rehearsals."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

Handler = Callable[[Mapping[str, Any]], Any]


class FakeProvider:
    def __init__(
        self,
        provider_id: str,
        capabilities: set[str],
        handlers: Mapping[str, Handler] | None = None,
    ) -> None:
        self.provider_id = provider_id
        self.capabilities = frozenset(capabilities)
        self.handlers = dict(handlers or {})

    def invoke(self, capability: str, request: Mapping[str, Any]) -> dict[str, Any]:
        if capability not in self.capabilities:
            return {
                "ok": False,
                "provider_id": self.provider_id,
                "error": {
                    "category": "unsupported_capability",
                    "message": f"{self.provider_id} does not advertise {capability}",
                },
            }
        handler = self.handlers.get(capability)
        try:
            value = handler(request) if handler else dict(request)
        except TimeoutError as exc:
            return {
                "ok": False,
                "provider_id": self.provider_id,
                "error": {"category": "timeout", "message": str(exc)},
            }
        except Exception as exc:  # provider boundary normalizes implementation failures
            return {
                "ok": False,
                "provider_id": self.provider_id,
                "error": {"category": "execution_failed", "message": str(exc)},
            }
        return {"ok": True, "provider_id": self.provider_id, "result": value}

from __future__ import annotations

from contextvars import ContextVar


current_client: ContextVar[object | None] = ContextVar("agentlens_current_client", default=None)
current_run: ContextVar[object | None] = ContextVar("agentlens_current_run", default=None)
current_step_stack: ContextVar[list[str]] = ContextVar("agentlens_current_step_stack", default=[])
default_client: ContextVar[object | None] = ContextVar("agentlens_default_client", default=None)

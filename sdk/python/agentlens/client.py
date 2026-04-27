from __future__ import annotations

import secrets
from contextlib import AbstractContextManager
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from agentlens.context import current_client, current_run, current_step_stack, default_client
from agentlens.exporters import HttpExporter
from agentlens.masking import Masker, default_mask_payload
from agentlens.types import StepPayload


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


@dataclass
class AgentLens:
    api_key: str
    project_id: str
    endpoint: str = "http://localhost:8000"
    environment: str = "local"
    enabled: bool = True
    timeout_ms: int = 2000
    fail_open: bool = True
    mask_pii: bool = True
    maskers: list[Masker] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.exporter = HttpExporter(
            endpoint=self.endpoint,
            api_key=self.api_key,
            timeout_ms=self.timeout_ms,
        )

    def add_masker(self, masker: Masker) -> None:
        self.maskers.append(masker)

    def configure(self) -> "AgentLens":
        default_client.set(self)
        return self

    def mask_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        masked = default_mask_payload(payload) if self.mask_pii else dict(payload)
        for masker in self.maskers:
            masked = masker(masked)
        return masked

    def run(self, name: str, input: dict[str, Any]) -> "RunContext":
        return RunContext(client=self, name=name, input=input)

    def _safe_call(self, fn: callable) -> None:
        if not self.enabled:
            return
        try:
            fn()
        except Exception:
            if not self.fail_open:
                raise


class RunContext(AbstractContextManager["RunContext"]):
    def __init__(self, client: AgentLens, name: str, input: dict[str, Any]) -> None:
        self.client = client
        self.name = name
        self.input = input
        self.run_id = f"run_{secrets.token_hex(8)}"
        self.started_at = _utc_now()
        self.output: dict[str, Any] = {}
        self.status = "running"

    def __enter__(self) -> "RunContext":
        current_client.set(self.client)
        current_run.set(self)
        current_step_stack.set([])
        payload = {
            "project_id": self.client.project_id,
            "run_id": self.run_id,
            "name": self.name,
            "environment": self.client.environment,
            "input": self.client.mask_payload(self.input),
            "metadata": {},
            "started_at": self.started_at.isoformat(),
        }
        self.client._safe_call(lambda: self.client.exporter.create_run(payload))
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is not None:
            self.status = "failed"
            self.output = {"error": str(exc)}
        elif self.status == "running":
            self.status = "success"
        payload = {
            "status": self.status,
            "output": self.client.mask_payload(self.output),
            "ended_at": _utc_now().isoformat(),
        }
        self.client._safe_call(lambda: self.client.exporter.end_run(self.run_id, payload))
        current_run.set(None)
        current_client.set(None)
        current_step_stack.set([])
        return None

    def set_output(self, output: dict[str, Any]) -> None:
        self.output = output

    def step(self, type: str, name: str, input: dict[str, Any]) -> "StepContext":
        return StepContext(run=self, type=type, name=name, input=input)


class StepContext(AbstractContextManager["StepContext"]):
    def __init__(self, run: RunContext, type: str, name: str, input: dict[str, Any]) -> None:
        self.run = run
        self.type = type
        self.name = name
        self.input = input
        self.output: dict[str, Any] = {}
        self.status = "success"
        self.step_id = f"step_{secrets.token_hex(8)}"
        self.started_at = _utc_now()
        self.parent_step_id: str | None = None

    def __enter__(self) -> "StepContext":
        stack = list(current_step_stack.get())
        self.parent_step_id = stack[-1] if stack else None
        stack.append(self.step_id)
        current_step_stack.set(stack)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is not None:
            self.status = "failed"
            self.output = {"error": str(exc)}

        ended_at = _utc_now()
        payload = StepPayload(
            step_id=self.step_id,
            parent_step_id=self.parent_step_id,
            type=self.type,
            name=self.name,
            status=self.status,
            input=self.run.client.mask_payload(self.input),
            output=self.run.client.mask_payload(self.output),
            started_at=self.started_at,
            ended_at=ended_at,
            latency_ms=int((ended_at - self.started_at).total_seconds() * 1000),
        )
        serializable = asdict(payload)
        serializable["started_at"] = self.started_at.isoformat()
        serializable["ended_at"] = ended_at.isoformat()
        self.run.client._safe_call(
            lambda: self.run.client.exporter.create_step(self.run.run_id, serializable)
        )
        stack = list(current_step_stack.get())
        if stack and stack[-1] == self.step_id:
            stack.pop()
        current_step_stack.set(stack)
        return None

    def set_output(self, output: dict[str, Any]) -> None:
        self.output = output

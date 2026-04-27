from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from agentlens.client import AgentLens


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return _json_safe(value)
    if value is None:
        return {}
    return {"value": _json_safe(value)}


def _export_trace(trace: Any) -> dict[str, Any]:
    exporter = getattr(trace, "export", None)
    if callable(exporter):
        exported = exporter()
        if isinstance(exported, dict):
            return _json_safe(exported)
    return {
        "id": getattr(trace, "trace_id", ""),
        "workflow_name": getattr(trace, "name", "Agent workflow"),
        "group_id": getattr(trace, "group_id", None),
        "metadata": _json_safe(getattr(trace, "metadata", None) or {}),
    }


def _export_span(span: Any) -> dict[str, Any]:
    exporter = getattr(span, "export", None)
    if callable(exporter):
        exported = exporter()
        if isinstance(exported, dict):
            return _json_safe(exported)
    return {
        "id": getattr(span, "span_id", ""),
        "trace_id": getattr(span, "trace_id", ""),
        "parent_id": getattr(span, "parent_id", None),
        "started_at": getattr(span, "started_at", None),
        "ended_at": getattr(span, "ended_at", None),
        "span_data": _json_safe(getattr(span, "span_data", {})),
        "error": _json_safe(getattr(span, "error", None)),
        "metadata": _json_safe(getattr(span, "trace_metadata", None) or {}),
    }


def _span_name(span_data: dict[str, Any], fallback_type: str) -> str:
    for key in ("name", "agent", "tool_name", "from_agent", "to_agent", "model"):
        value = span_data.get(key)
        if isinstance(value, str) and value:
            return value
    return fallback_type


def _normalize_step(exported: dict[str, Any]) -> dict[str, Any]:
    span_data = _as_dict(exported.get("span_data"))
    span_type = str(span_data.get("type") or "custom")

    input_payload: dict[str, Any] = {}
    for key in ("input", "arguments", "request", "data"):
        if key in span_data:
            input_payload[key] = _json_safe(span_data[key])

    output_payload: dict[str, Any] = {}
    for key in ("output", "response", "result"):
        if key in span_data:
            output_payload[key] = _json_safe(span_data[key])

    model_payload: dict[str, Any] = {}
    if "model" in span_data:
        model_payload["name"] = _json_safe(span_data["model"])
    if "model_config" in span_data:
        model_payload["config"] = _json_safe(span_data["model_config"])

    usage_payload = _as_dict(span_data.get("usage"))

    metadata = _as_dict(exported.get("metadata"))
    for key, value in span_data.items():
        if key not in {"type", "input", "output", "response", "result", "usage", "model", "model_config"}:
            metadata.setdefault(key, _json_safe(value))

    error_payload = exported.get("error")
    status = "failed" if error_payload else "success"

    return {
        "step_id": str(exported.get("id") or ""),
        "parent_step_id": exported.get("parent_id"),
        "type": span_type,
        "name": _span_name(span_data, span_type),
        "status": status,
        "input": input_payload,
        "output": output_payload,
        "model": model_payload,
        "usage": usage_payload,
        "metadata": metadata,
        "error": _json_safe(error_payload),
        "started_at": exported.get("started_at"),
        "ended_at": exported.get("ended_at"),
    }


@dataclass
class _TraceState:
    run_id: str
    workflow_name: str
    started_at: str
    metadata: dict[str, Any] = field(default_factory=dict)
    group_id: str | None = None
    error_count: int = 0
    last_output: dict[str, Any] = field(default_factory=dict)


def _utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


class OpenAIAgentsTracingProcessor:
    def __init__(self, client: AgentLens) -> None:
        self.client = client
        self._traces: dict[str, _TraceState] = {}

    def on_trace_start(self, trace: Any) -> None:
        exported = _export_trace(trace)
        run_id = str(exported.get("id") or getattr(trace, "trace_id", ""))
        workflow_name = str(exported.get("workflow_name") or getattr(trace, "name", "Agent workflow"))
        metadata = _as_dict(exported.get("metadata"))
        group_id = exported.get("group_id")
        started_at = _utc_now_iso()

        self._traces[run_id] = _TraceState(
            run_id=run_id,
            workflow_name=workflow_name,
            started_at=started_at,
            metadata=metadata,
            group_id=group_id if isinstance(group_id, str) else None,
        )

        payload = {
            "project_id": self.client.project_id,
            "run_id": run_id,
            "name": workflow_name,
            "environment": self.client.environment,
            "input": {
                "source": "openai_agents_sdk",
                "group_id": group_id,
            },
            "metadata": metadata | {"integration": "openai_agents_sdk"},
            "started_at": started_at,
        }

        self.client._safe_call(lambda: self.client.exporter.create_run(payload))

    def on_trace_end(self, trace: Any) -> None:
        exported = _export_trace(trace)
        run_id = str(exported.get("id") or getattr(trace, "trace_id", ""))
        state = self._traces.pop(run_id, None)
        if state is None:
            return

        output = {
            "source": "openai_agents_sdk",
            "final_output": state.last_output or {},
            "trace_metadata": state.metadata,
        }
        status = "failed" if state.error_count > 0 else "success"

        payload = {
            "status": status,
            "output": output,
            "ended_at": _utc_now_iso(),
        }
        self.client._safe_call(lambda: self.client.exporter.end_run(run_id, payload))

    def on_span_start(self, span: Any) -> None:
        return None

    def on_span_end(self, span: Any) -> None:
        exported = _export_span(span)
        run_id = str(exported.get("trace_id") or getattr(span, "trace_id", ""))
        state = self._traces.get(run_id)
        if state is None:
            return

        step = _normalize_step(exported)
        if step["output"]:
            state.last_output = step["output"]
        if step["status"] == "failed":
            state.error_count += 1

        started_at = step["started_at"] or "1970-01-01T00:00:00+00:00"
        ended_at = step["ended_at"] or started_at

        payload = {
            "step_id": step["step_id"],
            "parent_step_id": step["parent_step_id"],
            "type": step["type"],
            "name": step["name"],
            "status": step["status"],
            "input": step["input"],
            "output": step["output"],
            "model": step["model"],
            "usage": step["usage"],
            "metadata": step["metadata"],
            "error": step["error"],
            "started_at": started_at,
            "ended_at": ended_at,
            "latency_ms": _latency_ms(started_at, ended_at),
        }
        self.client._safe_call(lambda: self.client.exporter.create_step(run_id, payload))

    def shutdown(self) -> None:
        self._traces.clear()

    def force_flush(self) -> None:
        return None


def _latency_ms(started_at: str, ended_at: str) -> int:
    try:
        from datetime import datetime

        started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        ended = datetime.fromisoformat(ended_at.replace("Z", "+00:00"))
        return int((ended - started).total_seconds() * 1000)
    except Exception:
        return 0


def install_openai_agents_tracing(client: AgentLens) -> OpenAIAgentsTracingProcessor:
    try:
        from agents.tracing import add_trace_processor
    except ImportError as exc:
        raise ImportError(
            "OpenAI Agents SDK is not installed. Install it with `pip install openai-agents`."
        ) from exc

    processor = OpenAIAgentsTracingProcessor(client)
    add_trace_processor(processor)
    return processor

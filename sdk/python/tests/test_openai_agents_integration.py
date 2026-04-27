from agentlens.client import AgentLens
from agentlens.integrations.openai_agents import OpenAIAgentsTracingProcessor


class RecordingExporter:
    def __init__(self) -> None:
        self.runs: list[dict] = []
        self.steps: list[tuple[str, dict]] = []
        self.ends: list[tuple[str, dict]] = []

    def create_run(self, payload: dict) -> None:
        self.runs.append(payload)

    def create_step(self, run_id: str, payload: dict) -> None:
        self.steps.append((run_id, payload))

    def end_run(self, run_id: str, payload: dict) -> None:
        self.ends.append((run_id, payload))


class FakeTrace:
    def __init__(self) -> None:
        self.trace_id = "trace_demo_123"
        self.name = "Customer service workflow"
        self.group_id = "thread_42"
        self.metadata = {"customer_id": "cust_1"}

    def export(self) -> dict:
        return {
            "id": self.trace_id,
            "workflow_name": self.name,
            "group_id": self.group_id,
            "metadata": self.metadata,
        }


class FakeSpan:
    def __init__(self) -> None:
        self.trace_id = "trace_demo_123"
        self.span_id = "span_demo_1"
        self.parent_id = None
        self.started_at = "2026-01-01T00:00:00+00:00"
        self.ended_at = "2026-01-01T00:00:01+00:00"
        self.error = None
        self.trace_metadata = {"customer_id": "cust_1"}

    def export(self) -> dict:
        return {
            "id": self.span_id,
            "trace_id": self.trace_id,
            "parent_id": self.parent_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "span_data": {
                "type": "generation",
                "model": "gpt-4.1",
                "input": [{"role": "user", "content": "Help me reset my password"}],
                "output": [{"role": "assistant", "content": "Use the reset link"}],
                "usage": {"total_tokens": 42},
            },
            "error": self.error,
            "metadata": {"customer_id": "cust_1"},
        }


def test_openai_agents_processor_exports_trace_and_span() -> None:
    client = AgentLens(api_key="test", project_id="proj_1")
    exporter = RecordingExporter()
    client.exporter = exporter

    processor = OpenAIAgentsTracingProcessor(client)
    trace = FakeTrace()
    span = FakeSpan()

    processor.on_trace_start(trace)
    processor.on_span_end(span)
    processor.on_trace_end(trace)

    assert exporter.runs[0]["run_id"] == "trace_demo_123"
    assert exporter.runs[0]["name"] == "Customer service workflow"
    assert exporter.steps[0][0] == "trace_demo_123"
    assert exporter.steps[0][1]["type"] == "generation"
    assert exporter.steps[0][1]["model"]["name"] == "gpt-4.1"
    assert exporter.steps[0][1]["usage"]["total_tokens"] == 42
    assert exporter.ends[0][0] == "trace_demo_123"
    assert exporter.ends[0][1]["status"] == "success"

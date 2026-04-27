# AgentLens Python SDK

`aniket-agentlens-sdk` is the Python tracing SDK for AgentLens.

It lets another Python application instrument agent runs and steps with a small decorator-based API while sending trace data to a running AgentLens backend.

## Install

```bash
pip install aniket-agentlens-sdk
```

Import path:

```python
from agentlens import AgentLens, trace_agent, trace_step
```

The PyPI distribution name and the Python import name are intentionally different:

- install name: `aniket-agentlens-sdk`
- import name: `agentlens`

## Quick Start

```python
from agentlens import AgentLens, trace_agent, trace_step

AgentLens(
    api_key="al_sk_your_key",
    project_id="proj_your_project",
    endpoint="http://localhost:8000",
).configure()


@trace_step(type="tool_call", name="search_documents")
def search_documents(query: str) -> dict[str, object]:
    return {"matches": ["document_1", "document_2"], "query": query}


@trace_agent(name="knowledge_assistant_agent")
def run_agent(message: str) -> dict[str, object]:
    result = search_documents(message)
    return {"message": "done", "result": result}
```

## OpenAI Agents SDK Integration

Install both SDKs:

```bash
pip install aniket-agentlens-sdk openai-agents
```

Then register the AgentLens tracing processor:

```python
from agentlens import AgentLens, install_openai_agents_tracing

client = AgentLens(
    api_key="al_sk_your_key",
    project_id="proj_your_project",
    endpoint="http://localhost:8000",
).configure()

install_openai_agents_tracing(client)
```

This uses the OpenAI Agents SDK custom tracing processor hook so AgentLens receives the same traces and spans that the framework emits.

## Runtime Flow

1. `AgentLens(...).configure()` sets the default SDK client.
2. `@trace_agent` creates a traced run.
3. `@trace_step` creates nested steps under the current run.
4. The SDK sends HTTP requests to the AgentLens backend.
5. The backend stores, masks, and analyzes the trace for display in the dashboard.

## Requirements

- Python `>=3.11`
- A running AgentLens backend
- A valid AgentLens `project_id`
- A valid AgentLens ingestion API key

## Links

- Repository: https://github.com/aniketgopal/agentlens
- Documentation: https://github.com/aniketgopal/agentlens/tree/main/docs

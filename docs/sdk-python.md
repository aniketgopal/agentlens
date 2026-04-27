# Python SDK

The Python SDK is the current ingestion path for AgentLens.

Location: [`../sdk/python`](../sdk/python)

PyPI distribution name: `aniket-agentlens-sdk`  
Python import name: `agentlens`

## Install

```bash
pip install aniket-agentlens-sdk
```

Published package page: https://pypi.org/project/aniket-agentlens-sdk/

## Goals

- minimal integration effort
- fail-open behavior by default
- decorator-based tracing
- step and run context managers
- local masking before export

## Basic Usage

```python
from agentlens import AgentLens, trace_agent, trace_step

AgentLens(
    api_key="al_sk_your_key",
    project_id="proj_your_project",
    endpoint="http://localhost:8000",
).configure()

@trace_step(type="tool_call", name="search_candidates")
def search_candidates(query: str):
    return {"matches": ["candidate_1"], "query": query}

@trace_agent(name="candidate_screening_agent")
def run_agent(message: str):
    return {"answer": search_candidates(message)}
```

## Current Features

- `AgentLens(...).configure()`
- `@trace_agent`
- `@trace_step`
- context-based run and step export
- payload masking
- fail-open export behavior

## Current Gaps

- framework-specific integrations are still limited
- async flows need broader verification coverage
- buffering/retry behavior is still minimal

## Design Rule

The SDK must never break the user application by default when the AgentLens backend is unavailable.

## Maintainer Note

SDK release flow is documented in [`./sdk-release.md`](./sdk-release.md).

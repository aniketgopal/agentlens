# AgentLens

AgentLens is an open-source reliability, debugging, evaluation, and security platform for AI agents.

[![PyPI](https://img.shields.io/pypi/v/aniket-agentlens-sdk)](https://pypi.org/project/aniket-agentlens-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/aniket-agentlens-sdk)](https://pypi.org/project/aniket-agentlens-sdk/)

It is designed to give developers a local-first way to:
- trace agent runs and steps
- inspect prompts, tool calls, outputs, and errors
- flag basic security issues
- run simple evaluations against stored runs
- manage projects and ingestion API keys

## Current Scope

What works today:
- project creation and API key generation
- Python SDK with fail-open tracing
- OpenAI Agents SDK integration via tracing processor
- run and step ingestion
- run explorer and run inspector UI
- security findings with status actions
- evaluation MVP with stored results
- server-side masking and payload-size enforcement

What is still in progress:
- additional framework integrations beyond OpenAI Agents SDK
- more evaluation types
- broader security rule coverage
- stronger test coverage and frontend polish

## Why Use AgentLens

AgentLens is most useful when an AI agent is already running in production or internal workflows, but the team cannot answer basic debugging questions quickly:
- what input triggered this run
- which tool or model call produced the bad result
- where sensitive data leaked into a response
- whether a change improved or regressed behavior

This initial version is strongest for teams who want a local-first Python tracing stack with built-in security and evaluation signals, without building internal tooling from scratch.

## Documentation

- [Getting Started](./docs/getting-started.md)
- [Architecture](./docs/architecture.md)
- [Python SDK](./docs/sdk-python.md)
- [SDK Release](./docs/sdk-release.md)
- [API Reference](./docs/api-reference.md)
- [Security Model](./docs/security-model.md)
- [Deployment](./docs/deployment.md)

## Screenshots

### Runs Explorer

![Runs Explorer](./frontend/public/screenshots/runs-overview.png)

### Run Inspector

![Run Inspector](./frontend/public/screenshots/run-inspector.png)

### Security Findings

![Security Findings](./frontend/public/screenshots/security-findings.png)

### Project Management

![Project Management](./frontend/public/screenshots/projects-page.png)

## Architecture

Current runtime path:

`Python SDK -> FastAPI -> MongoDB -> Next.js`

See [`docs/architecture.md`](./docs/architecture.md) for the high-level layout.

## Repository Layout

- `backend/`: FastAPI collector API and application services
- `sdk/python/`: Python tracing SDK
- `frontend/`: Next.js dashboard
- `examples/`: simple example agent usage
- `docs/`: supplementary docs
- `docker-compose.yml`: local development stack

## Quick Start

### 1. Configure environment

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Start the stack

```bash
docker compose up --build -d
```

Services:
- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`

Optional convenience:

```bash
make up
```

### 3. Create a project and API key

Open `http://localhost:3000/projects`.

1. Create a project.
2. Generate an API key for that project.
3. Copy the API key when it is shown. It is only displayed once.

### 4. Send a traced run

Install the published SDK:

```bash
pip install aniket-agentlens-sdk
```

Then use the example in [`examples/simple-agent/main.py`](./examples/simple-agent/main.py) or instrument your own app.

Important:
- install name: `aniket-agentlens-sdk`
- import name: `agentlens`

Example:

```python
from agentlens import AgentLens, trace_agent, trace_step

AgentLens(
    api_key="al_sk_your_key",
    project_id="proj_your_project",
    endpoint="http://localhost:8000",
).configure()

@trace_step(type="tool_call", name="search_documents")
def search_documents(query: str):
    return {"matches": ["document_1"], "query": query}

@trace_agent(name="knowledge_assistant_agent")
def run_agent(message: str):
    return {"answer": search_documents(message)}
```

### 4a. Seed the full demo flow

To create a project, generate an API key, send a normal trace, and send a security-focused trace:

```bash
docker compose exec -T backend python /app/scripts/bootstrap_demo.py
```

Optional convenience:

```bash
make seed-demo
```

This seeds:
- a normal traced run from [`examples/simple-agent/main.py`](./examples/simple-agent/main.py)
- a security-focused run from [`examples/security-demo/main.py`](./examples/security-demo/main.py)

### 4b. Use OpenAI Agents SDK

AgentLens can also mirror traces from the OpenAI Agents SDK using a custom tracing processor.

```bash
pip install aniket-agentlens-sdk openai-agents
```

Example:
- [`examples/openai-agents/main.py`](./examples/openai-agents/main.py)

### 5. Inspect the results

Use the UI:
- `/` for runs
- `/dashboard` for overview
- `/security` for findings
- `/evaluations` for evaluations

The seeded security demo intentionally produces prompt-injection and sensitive-data findings so the security workflow is visible immediately.

## Local Development

### Docker-first path

This is the primary supported path:

```bash
docker compose up --build -d
```

### Backend

If you already have Python tooling locally:

```bash
cd backend
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### SDK

```bash
cd sdk/python
pip install -e .
```

For a published install instead of editable local development:

```bash
pip install aniket-agentlens-sdk
```

## Configuration

Important environment variables:

- `AGENTLENS_MONGODB_URI`
- `AGENTLENS_MONGODB_DATABASE`
- `AGENTLENS_MASK_PII`
- `AGENTLENS_MAX_PAYLOAD_BYTES`
- `NEXT_PUBLIC_AGENTLENS_API_BASE_URL`

See [`.env.example`](./.env.example) for defaults.

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run build
```

SDK:

```bash
cd sdk/python
pip install -e .[dev]
pytest tests
python -m build
```

## SDK Release

The Python SDK is published to PyPI as `aniket-agentlens-sdk`.

Public install:

```bash
pip install aniket-agentlens-sdk
```

Maintainer flow:

1. Update `version` in [`sdk/python/pyproject.toml`](./sdk/python/pyproject.toml)
2. Push the change to `main`
3. Trigger [`.github/workflows/publish-sdk.yml`](./.github/workflows/publish-sdk.yml) from GitHub Actions or push a tag like `sdk-v0.1.1`

Trusted Publishing is configured through GitHub Actions, so no long-lived PyPI token is required in the repository.

## Roadmap

Near-term priorities:

- frictionless onboarding and seeded demo flow
- additional framework integrations beyond OpenAI Agents SDK
- stronger debugging ergonomics around nested runs and step context
- stronger evaluation coverage
- broader security rule set
- improved frontend polish and testing
- dependency and CI hardening

Longer-term directions:

- prompt/version management
- simulation workflows
- deeper audit and decision records
- queue-based ingestion path
- larger-scale storage split for analytics

## Security Notes

- raw API keys are never stored
- API keys are shown once at creation time
- payloads are masked server-side before persistence
- oversized payloads are rejected with HTTP `413`

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## License

Apache-2.0

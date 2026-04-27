# Getting Started

This guide walks through the shortest path to a working local AgentLens setup.

## Prerequisites

- Docker
- Docker Compose

The Docker path is the primary supported setup for this repository.

## Step 1: Configure environment

```bash
cp .env.example .env
```

Default values are suitable for local development.

## Step 2: Start the stack

```bash
docker compose up --build -d
```

Default local endpoints:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- MongoDB: `mongodb://localhost:27017`

## Step 3: Create a project

Open `http://localhost:3000/projects`.

1. Create a project.
2. Generate an API key for that project.
3. Copy the key when displayed. It is shown once.

## Step 4: Send a traced run

Use the example in [`../examples/simple-agent/main.py`](../examples/simple-agent/main.py) or instrument your own Python code with the SDK.

## Step 5: Inspect the data

Open:

- `/` for runs
- `/dashboard` for project metrics
- `/security` for findings
- `/evaluations` for evaluation results

## First Troubleshooting Checks

- If the frontend loads but no data appears, create a project first.
- If ingestion fails, confirm the backend is reachable at `http://localhost:8000`.
- If traces are rejected, check payload size and masking behavior in the backend logs.

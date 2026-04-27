# API Reference

This is the current MVP API surface.

## Projects

### `GET /api/v1/projects`

List projects.

### `POST /api/v1/projects`

Create a project.

Request:

```json
{
  "name": "Operations Assistant",
  "description": "Internal workflow tracing project"
}
```

### `POST /api/v1/projects/{project_id}/api-keys`

Generate a new API key for a project.

## Runs

### `POST /api/v1/runs`

Create a run.

Requires `Authorization: Bearer <api-key>`.

### `POST /api/v1/runs/{run_id}/steps`

Ingest a traced step.

Requires `Authorization: Bearer <api-key>`.

### `PATCH /api/v1/runs/{run_id}/end`

Finalize a run.

Requires `Authorization: Bearer <api-key>`.

### `GET /api/v1/runs?project_id=<id>`

List runs for a project.

### `GET /api/v1/runs/{run_id}`

Get run detail, including ordered steps.

## Security

### `GET /api/v1/security/findings?project_id=<id>`

List security findings.

### `PATCH /api/v1/security/findings/{finding_id}`

Update finding status.

Allowed statuses:

- `open`
- `false_positive`
- `resolved`

## Evaluations

### `POST /api/v1/evaluations/run`

Run a stored evaluation against a run.

Request:

```json
{
  "run_id": "run_123",
  "required_terms": ["approved"],
  "forbidden_terms": ["salary promise"],
  "required_output_keys": ["answer"]
}
```

### `GET /api/v1/evaluations?project_id=<id>`

List stored evaluations for a project.

## Notes

- responses are wrapped in a common JSON envelope
- server-side masking is applied before persistence
- oversized payloads are rejected with HTTP `413`

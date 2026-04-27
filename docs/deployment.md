# Deployment

## Recommended Local Deployment

Use Docker Compose:

```bash
docker compose up --build -d
```

## Services

- `frontend`
- `backend`
- `mongodb`

## Environment

Primary variables:

- `AGENTLENS_MONGODB_URI`
- `AGENTLENS_MONGODB_DATABASE`
- `AGENTLENS_API_HOST`
- `AGENTLENS_API_PORT`
- `AGENTLENS_MASK_PII`
- `AGENTLENS_MAX_PAYLOAD_BYTES`
- `NEXT_PUBLIC_AGENTLENS_API_BASE_URL`

## Production Notes

This repository is currently optimized for local and small-team use.

Before productionizing:

- add proper secret management
- add stronger auth and key lifecycle controls
- add monitoring and alerting
- add a real backup strategy for MongoDB
- review frontend and backend dependency upgrade posture

## CI/CD Notes

The repository includes basic GitHub Actions workflows for backend, frontend, and SDK sanity checks.

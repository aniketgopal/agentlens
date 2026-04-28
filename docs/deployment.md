# Deployment

## Recommended Local Deployment

Use Docker Compose:

```bash
docker compose up --build -d
```

Optional convenience:

```bash
make up
```

## Services

- `frontend`
- `backend`
- `mongodb`
- `scripts/bootstrap_demo.py` available inside the backend container for seeded demo setup

## Environment

Primary variables:

- `AGENTLENS_MONGODB_URI`
- `AGENTLENS_MONGODB_DATABASE`
- `AGENTLENS_API_HOST`
- `AGENTLENS_API_PORT`
- `AGENTLENS_MASK_PII`
- `AGENTLENS_MAX_PAYLOAD_BYTES`
- `NEXT_PUBLIC_AGENTLENS_API_BASE_URL`

## Demo Bootstrap

After the stack is up, you can seed a reproducible project and demo traces:

```bash
docker compose exec -T backend python /app/scripts/bootstrap_demo.py
```

Optional convenience:

```bash
make seed-demo
```

## Production Notes

This repository is currently optimized for local and small-team use.

Before productionizing:

- add proper secret management
- add stronger auth and key lifecycle controls
- add monitoring and alerting
- add a real backup strategy for MongoDB
- review frontend and backend dependency upgrade posture

## CI/CD Notes

The repository includes GitHub Actions workflows for:

- backend CI
- frontend build validation
- SDK CI
- SDK Trusted Publishing to PyPI

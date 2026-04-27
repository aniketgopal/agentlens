# Contributing

## Development Expectations

- Keep changes scoped and reviewable.
- Add tests with new backend behavior.
- Do not log secrets or unmasked payloads.
- Prefer Docker for local development unless you already have the required local toolchain.

## Local Setup

```bash
cp .env.example .env
docker compose up --build -d
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000`

## Before Opening a PR

- Run backend tests if you changed backend code.
- Run a frontend build if you changed frontend code.
- Update docs when the user-facing workflow changes.
- Avoid unrelated formatting-only changes.

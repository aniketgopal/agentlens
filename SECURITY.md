# Security Policy

## Principles

- Never store raw API keys.
- Mask sensitive payloads before persistence.
- Reject oversized ingestion payloads.
- Keep secrets out of logs and test fixtures.

## Reporting

Report vulnerabilities privately to the repository maintainers rather than opening a public issue.

## Current Safeguards

- API keys are hashed before storage.
- Server-side masking is applied on run and step payloads.
- Basic security findings are generated from stored traces.

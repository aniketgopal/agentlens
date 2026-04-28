# Security Model

AgentLens is not a complete security platform yet, but it already applies several defensive rules in the ingestion path.

## Current Controls

### API key handling

- raw API keys are shown once
- API keys are hashed before storage
- ingestion routes require bearer-token authentication

### Payload masking

The backend masks common sensitive values before persistence, including:

- email addresses
- phone-like values
- card-like values
- API key patterns
- JWT-like strings
- secret/token/password fields

### Payload limits

Oversized ingestion payloads are rejected with HTTP `413`.

Config:

- `AGENTLENS_MAX_PAYLOAD_BYTES`

### Security findings

The MVP scanner detects basic patterns such as:

- prompt injection attempts
- system prompt leakage
- internal-notes exposure

## Current Limitations

- rule coverage is intentionally narrow
- masking is regex-based and not domain-specific
- findings are heuristic, not authoritative
- no multi-tenant auth model exists yet
- field-level evidence and deeper semantic analysis are not implemented yet

## Recommended Usage

Treat AgentLens as development and internal-debugging infrastructure until you complete your own production review.

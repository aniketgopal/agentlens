# Architecture

Initial MVP flow:

`Python SDK -> FastAPI -> MongoDB -> Next.js`

## Components

### SDK

The Python SDK captures runs and steps, masks payloads locally where configured, and exports them to the backend.

### Backend

The FastAPI backend handles:

- project and API key management
- run and step ingestion
- server-side masking
- payload-size enforcement
- security finding generation
- evaluation record storage

### Storage

MongoDB is the current persistence layer for:

- projects
- API keys
- runs
- trace steps
- security findings
- evaluations

### Frontend

The Next.js frontend provides:

- project management
- run explorer
- run inspector
- security findings review
- evaluation execution and history

## Current Non-Goals

- full SaaS multitenancy
- advanced RBAC
- queue-based ingestion pipeline
- high-volume analytics storage

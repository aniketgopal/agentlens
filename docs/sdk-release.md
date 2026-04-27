# SDK Release

This document covers the release flow for the published Python SDK.

## Published Package

- PyPI distribution: `aniket-agentlens-sdk`
- Python import: `agentlens`

Users install:

```bash
pip install aniket-agentlens-sdk
```

Users import:

```python
from agentlens import AgentLens, trace_agent, trace_step
```

## Versioning

Update the SDK version in [`../sdk/python/pyproject.toml`](../sdk/python/pyproject.toml):

```toml
[project]
version = "0.1.1"
```

## Pre-release Checks

From `sdk/python`:

```bash
pip install -e .[dev]
pytest tests
python -m build
python -m twine check dist/*
```

## Publish Flow

The repository uses GitHub Actions Trusted Publishing via [`.github/workflows/publish-sdk.yml`](../.github/workflows/publish-sdk.yml).

You can publish in either of these ways:

1. Manual workflow dispatch from GitHub Actions
2. Push a tag matching `sdk-v*`

Example:

```bash
git tag sdk-v0.1.1
git push origin sdk-v0.1.1
```

## PyPI Trusted Publisher

PyPI should be configured to trust:

- owner: `aniketgopal`
- repository: `agentlens`
- workflow: `.github/workflows/publish-sdk.yml`
- environment: `pypi`

## Notes

- The package name `agentlens` is already taken on PyPI, so this repository publishes the SDK as `aniket-agentlens-sdk`.
- The import path remains `agentlens`, which is why installation and import names differ.

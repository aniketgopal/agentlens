from __future__ import annotations

from typing import Any

import requests


class HttpExporter:
    def __init__(self, endpoint: str, api_key: str, timeout_ms: int = 2000) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout_ms / 1000

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_run(self, payload: dict[str, Any]) -> None:
        requests.post(
            f"{self.endpoint}/api/v1/runs",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        ).raise_for_status()

    def create_step(self, run_id: str, payload: dict[str, Any]) -> None:
        requests.post(
            f"{self.endpoint}/api/v1/runs/{run_id}/steps",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        ).raise_for_status()

    def end_run(self, run_id: str, payload: dict[str, Any]) -> None:
        requests.patch(
            f"{self.endpoint}/api/v1/runs/{run_id}/end",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        ).raise_for_status()

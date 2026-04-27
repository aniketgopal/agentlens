from __future__ import annotations

import json
import re
from typing import Any

from fastapi import HTTPException, status

from app.core.config import settings


class MaskingService:
    def mask_payload(self, payload: Any) -> Any:
        if not settings.mask_pii:
            return payload
        return self._walk("", payload)

    def validate_payload_size(self, field_name: str, payload: Any) -> None:
        encoded = json.dumps(payload, default=str).encode("utf-8")
        if len(encoded) > settings.max_payload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"{field_name} exceeds max payload size of {settings.max_payload_bytes} bytes",
            )

    def sanitize_and_validate(self, field_name: str, payload: Any) -> Any:
        masked = self.mask_payload(payload)
        self.validate_payload_size(field_name, masked)
        return masked

    def _walk(self, key: str, value: Any) -> Any:
        if isinstance(value, dict):
            return {nested_key: self._walk(nested_key, nested_value) for nested_key, nested_value in value.items()}
        if isinstance(value, list):
            return [self._walk(key, item) for item in value]
        if isinstance(value, str):
            return self._mask_scalar(key, value)
        return value

    def _mask_scalar(self, key: str, value: str) -> str:
        lowered = key.lower()
        if any(token in lowered for token in ("password", "secret", "token", "api_key", "apikey")):
            return "***"

        masked = value
        masked = re.sub(
            r"([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*@([A-Za-z0-9.-]+\.[A-Za-z]{2,})",
            r"\1***@\2",
            masked,
        )
        masked = re.sub(r"\b(?:\+?\d[\d -]{8,}\d)\b", "***", masked)
        masked = re.sub(r"\b(?:\d[ -]*?){13,19}\b", "***", masked)
        masked = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "***", masked)
        masked = re.sub(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+\b", "***", masked)
        return masked

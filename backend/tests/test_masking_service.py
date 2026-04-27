from fastapi import HTTPException

from app.services.masking_service import MaskingService


def test_masking_service_masks_common_sensitive_values() -> None:
    service = MaskingService()
    masked = service.mask_payload(
        {
            "email": "john@example.com",
            "password": "super-secret",
            "message": "call me at +1 415 555 1212 with sk-secret123456",
            "jwt": "eyJabc.def.ghi",
        }
    )
    assert masked["email"] == "j***@example.com"
    assert masked["password"] == "***"
    assert "***" in masked["message"]
    assert masked["jwt"] == "***"


def test_validate_payload_size_rejects_large_payload(monkeypatch) -> None:
    monkeypatch.setattr("app.services.masking_service.settings.max_payload_bytes", 10)
    service = MaskingService()
    try:
        service.validate_payload_size("run.output", {"answer": "this is too large"})
    except HTTPException as exc:
        assert exc.status_code == 413
    else:
        raise AssertionError("Expected HTTPException for oversized payload")

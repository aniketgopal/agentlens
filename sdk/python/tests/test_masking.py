from agentlens.masking import default_mask_payload


def test_default_mask_payload_masks_email_and_password() -> None:
    payload = {
        "email": "john@example.com",
        "password": "super-secret",
        "nested": {"token": "sk-secret123456"},
    }
    masked = default_mask_payload(payload)
    assert masked["email"] == "j***@example.com"
    assert masked["password"] == "***"
    assert masked["nested"]["token"] == "***"

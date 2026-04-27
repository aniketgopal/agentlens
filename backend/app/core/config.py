from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "agentlens"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    mask_pii: bool = True
    max_payload_bytes: int = 32768

    model_config = SettingsConfigDict(
        env_prefix="AGENTLENS_",
        case_sensitive=False,
    )


settings = Settings()

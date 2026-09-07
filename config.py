from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    environment: Literal["development", "production"] = "development"
    lboro_auth_token: str
    contact_email: str | None = None


config = Config()  # type: ignore (values are loaded from .env at runtime)

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    environment: Literal["development", "production"] = "development"
    lboro_username: str
    lboro_password: str


config = Config()  # type: ignore (values are loaded from .env at runtime)

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenConfig(BaseSettings):
    secret_key: str = Field()
    algorithm: Literal["HS256"] = "HS256"
    expire_in_minutes: int = 10

    model_config = SettingsConfigDict(env_prefix="JWT_")


class SessionConfig(BaseSettings):
    expire_in_days: int = 7
    token_len: int = 32

    model_config = SettingsConfigDict(env_prefix="SESSION_")


class ApiTokenConfig(BaseSettings):
    token_len: int = 64

    model_config = SettingsConfigDict(env_prefix="API_TOKEN_")

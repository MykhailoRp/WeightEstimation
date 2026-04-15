from pydantic_settings import BaseSettings, SettingsConfigDict


class _ServiceConfig(BaseSettings):
    name: str = "common"
    json_log: bool = False

    model_config = SettingsConfigDict(env_prefix="SERVICE_")


ServiceConfig = _ServiceConfig()

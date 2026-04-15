from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiDocConfig(BaseSettings):
    username: str = "admin"
    password: str = "admin"

    model_config = SettingsConfigDict(env_prefix="API_DOC_")

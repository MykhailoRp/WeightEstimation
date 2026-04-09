from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailConfig(BaseSettings):
    system_sender: str | None = None
    system_address: str
    password: str

    server: str = "smtp.gmail.com"
    port: int = 587

    model_config = SettingsConfigDict(env_prefix="EMAIL_")

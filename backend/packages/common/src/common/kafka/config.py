from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaConfig(BaseSettings):
    brokers: list[str] = Field(default_factory=lambda: ["kafka://localhost:9092"])

    model_config = SettingsConfigDict(env_prefix="KAFKA_")

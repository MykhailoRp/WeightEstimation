from pydantic_settings import BaseSettings, SettingsConfigDict

from common.types import FileId, WeightClassId


class StorageCongfig(BaseSettings):
    access_key_id: str = "rustfsadmin"
    secret_access_key: str = "rustfsadmin"

    endpoint_url: str = "http://localhost:9000"
    region_name: str = "us-east-1"

    bucket: str = "main"

    model_config = SettingsConfigDict(env_prefix="S3_")

    def get_uploads(self, file_id: FileId, /) -> str:
        return f"uploads/{file_id}"

    def get_weight_class_video(self, weight_class_id: WeightClassId, /) -> str:
        return f"weight_classification/{weight_class_id}/video"

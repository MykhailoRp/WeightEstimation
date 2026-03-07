from pydantic import BaseModel

from common.types import FileId


class HealthCheck(BaseModel):
    status: int
    text: str


class FileRespose(BaseModel):
    file_id: FileId

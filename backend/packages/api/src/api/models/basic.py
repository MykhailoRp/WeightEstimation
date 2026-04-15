from pydantic import BaseModel

from common.types import FileId


class HealthCheck(BaseModel):
    status: int
    text: str


class FileRespose(BaseModel):
    file_id: FileId


class Paginated(BaseModel):
    page: int = 0
    size: int = 10

    @property
    def offset(self) -> int:
        return self.page * self.size


class ListResponse[T: BaseModel](BaseModel):
    items: list[T]
    total_count: int

from pydantic import BaseModel


class ApiException(BaseModel):
    detail: str

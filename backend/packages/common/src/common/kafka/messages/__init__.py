from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseMessage(BaseModel):
    @staticmethod
    @abstractmethod
    def key(*args: Any, **kwargs: Any) -> str | None: ...

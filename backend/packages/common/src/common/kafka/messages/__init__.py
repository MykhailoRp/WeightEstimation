from abc import abstractmethod
from typing import Any

from faust import Record


class BaseMessage(Record, abstract=True):
    @staticmethod
    @abstractmethod
    def key(*args: Any, **kwargs: Any) -> bytes: ...

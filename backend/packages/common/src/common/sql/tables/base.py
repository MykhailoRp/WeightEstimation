from typing import Any

from sqlalchemy.orm import DeclarativeBase

from common.sql.utils import model_instance_to_dict


class Base(DeclarativeBase):
    def dict(
        self,
        *,
        include: set[str] | None = None,
        exclude: set[str] | None = None,
        exclude_none: bool = False,
        exclude_unloaded: bool = True,
    ) -> dict[str, Any]:
        return model_instance_to_dict(self, include=include, exclude=exclude, exclude_none=exclude_none, exclude_unloaded=exclude_unloaded)

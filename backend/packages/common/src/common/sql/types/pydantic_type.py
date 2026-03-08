from __future__ import annotations

from typing import TYPE_CHECKING, Any, final, override

import sqlalchemy as sa
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from typing import Any

    from pydantic import BaseModel
    from sqlalchemy import Dialect
    from sqlalchemy.sql.type_api import TypeEngine


# --------------------------------------------------------------------------------------
# Define pydantic-alchemy specific types (once per application)
# --------------------------------------------------------------------------------------


@final
class PydanticJSON(sa.types.TypeDecorator):
    """JSON(B) column type that encodes/decodes the value using Pydantic TypeAdapter

    SAVING:
    - Uses SQLAlchemy JSON type under the hood.
    - Acceps any type supported by Pydantic's TypeAdapter and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Validates the dict using the Type Adapter.
    """

    # If you intend to use this class with one dialect only,
    # you could pick a type from the specific dialect for
    # simplicity sake.
    #
    # E.g., if you work with PostgreSQL, you can consider using
    # sqlalchemy.dialects.postgresql.JSONB instead of a
    # generic sa.types.JSON
    # Ref: https://www.postgresql.org/docs/13/datatype-json.html
    #
    # Otherwise, you should implement the `load_dialect_impl`
    # method to handle different dialects. In this case, the
    # impl variable can reference TypeEngine as a placeholder.
    impl = sa.types.JSON

    def __init__(self, pydantic_type: type) -> None:
        super().__init__()

        # Wrap the type in a TypeAdapter, so that anything can be validated
        self.type_adapter = TypeAdapter(pydantic_type)  # type: ignore[var-annotated]

    @override
    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[JSONB | sa.JSON]:
        # You should implement this method to handle different dialects
        # if you intend to use this class with more than one.
        # E.g., use JSONB for PostgreSQL and the generic JSON type for
        # other databases.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(sa.JSON())

    @override
    def process_bind_param(
        self,
        value: BaseModel | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        return self.type_adapter.dump_python(value, mode="json")  # type: ignore[no-any-return]

    @override
    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> BaseModel | None:
        return self.type_adapter.validate_python(value)  # type: ignore[no-any-return]

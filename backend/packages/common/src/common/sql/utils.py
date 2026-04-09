from typing import Any

from sqlalchemy.orm import ColumnProperty, DeclarativeBase, InstanceState, Mapper, attributes, object_mapper


def _should_include(
    column_name: str,
    column_prop: ColumnProperty,
    column_value: Any,
    instance_state: InstanceState,
    *,
    include: set[str],
    exclude: set[str],
    exclude_none: bool,
    exclude_unloaded: bool,
) -> bool:
    if column_name in include:
        # if the column name was specified in the "include" set, we will include it
        return True
    if column_name in exclude:
        # if the column name was specified in the "exclude" set, we will exclude it
        return False
    if exclude_unloaded and column_name in instance_state.unloaded:
        # if exclude_unloaded was specified and the column name is unloaded, we will exclude it
        return False

    if column_value is None and exclude_none:
        # if the column is none and exclude_none was specified, we will exclude it
        return False

    return True


def model_instance_to_dict(
    instance: DeclarativeBase,
    *,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
    exclude_none: bool = False,
    exclude_unloaded: bool = True,
) -> dict[str, Any]:
    if exclude is None:
        exclude = set()
    if include is None:
        include = set()
    mapper: Mapper = object_mapper(instance)
    instance_state = attributes.instance_state(instance)
    instance_dict = {}
    for column_name, column_prop in mapper.column_attrs.items():
        column_value = getattr(instance, column_name)
        if _should_include(
            column_name,
            column_prop,
            column_value,
            instance_state,
            include=include,
            exclude=exclude,
            exclude_none=exclude_none,
            exclude_unloaded=exclude_unloaded,
        ):
            instance_dict[column_name] = column_value

    return instance_dict

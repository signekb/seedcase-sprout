import polars as pl

from seedcase_sprout.core.get_nested_attr import get_nested_attr
from seedcase_sprout.core.properties import ResourceProperties


def _check_column_names(
    data: pl.DataFrame, resource_properties: ResourceProperties
) -> str:
    """Checks that column names in `data` match those in `resource_properties`.

    Columns may appear in any order.

    Args:
        data: The data to check.
        resource_properties: The resource properties to check against.

    Returns:
        The data if the column names match.

    Raises:
        ValueError: If the column names don't match the names in
            `resource_properties`.
    """
    columns_in_data = data.schema.names()
    columns_in_resource = [
        field.name
        for field in get_nested_attr(resource_properties, "schema.fields", default=[])
    ]
    extra_columns_in_data = [
        name for name in columns_in_data if name not in columns_in_resource
    ]
    missing_columns_in_data = [
        name for name in columns_in_resource if name not in columns_in_data
    ]

    if extra_columns_in_data or missing_columns_in_data:
        raise ValueError(
            _format_column_name_error_message(
                extra_columns_in_data, missing_columns_in_data
            )
        )

    return data


def _format_column_name_error_message(
    extra_columns_in_data: list[str], missing_columns_in_data: list[str]
) -> str:
    message = (
        "Column names in the data do not match column names in the resource properties:"
    )
    if extra_columns_in_data:
        message += f"\n- Unexpected column(s) in data: {extra_columns_in_data}"
    if missing_columns_in_data:
        message += f"\n- Missing column(s) in data: {missing_columns_in_data}"
    return message

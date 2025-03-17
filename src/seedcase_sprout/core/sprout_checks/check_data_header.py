import polars as pl

from seedcase_sprout.core.get_nested_attr import get_nested_attr
from seedcase_sprout.core.properties import ResourceProperties


def check_data_header(
    data: pl.DataFrame, resource_properties: ResourceProperties
) -> pl.DataFrame:
    """Checks that column names in the data frame match column names in the properties.

    Args:
        data: The data frame to check.
        resource_properties: The resource properties to check against.

    Returns:
        The data frame, if the column names match.

    Raises:
        ValueError: If the header doesn't match the expected column names.
    """
    data_columns = data.schema.names()
    expected_columns = [
        field.name
        for field in get_nested_attr(resource_properties, "schema.fields", default=[])
    ]
    if data_columns != expected_columns:
        raise ValueError(
            "Column names in the data frame do not match column names in the resource "
            f"properties. Expected {expected_columns}, but found {data_columns}."
        )
    return data

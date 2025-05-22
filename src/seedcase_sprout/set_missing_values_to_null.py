import polars as pl

from seedcase_sprout.get_nested_attr import get_nested_attr
from seedcase_sprout.properties import (
    FieldProperties,
    ResourceProperties,
)


def set_missing_values_to_null(
    data: pl.DataFrame, resource_properties: ResourceProperties
):
    """Sets missing values to null.

    Uses the resource properties to locate missing values in the data frame and sets
    them to null.

    Args:
        data: The data frame to process.
        resource_properties: The resource properties describing the data.

    Returns:
        The updated data frame with missing values set to null.
    """
    fields: list[FieldProperties] = get_nested_attr(
        resource_properties, "schema.fields", default=[]
    )

    schema_missing_values = get_nested_attr(
        resource_properties, "schema.missing_values", default=[""]
    )
    return data.with_columns(
        pl.col(field.name).replace(
            old=schema_missing_values
            if field.missing_values is None
            # As per Frictionless standard, field-level missing values overrides
            # the schema-level missing values.
            else field.missing_values,
            new=None,
        )
        for field in fields
    )

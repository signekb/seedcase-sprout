from typing import Callable

import polars as pl

from seedcase_sprout.core.get_nested_attr import get_nested_attr
from seedcase_sprout.core.properties import (
    FieldProperties,
    FieldType,
    ResourceProperties,
)
from seedcase_sprout.core.sprout_checks.check_properties import (
    check_resource_properties,
)


def check_data(
    data: pl.DataFrame, resource_properties: ResourceProperties
) -> pl.DataFrame:
    """Checks that the DataFrame matches the requirements in the resource properties.

    Runs a few checks to compare between the data and the properties on the items:

    | Data | Properties |
    |:------|:------------|
    | Column names | `field.name` |
    | Column types | `field.types` |
    | Column values' types | `field.types` |
    | Column values' constraints | `field.constraints` |

    Error messages output generally in the format of:

    > # {data item}:
    >
    > There is a mismatch found:
    >
    > - In the properties: {mismatch}
    > - In the data: {mismatch}

    Args:
        data: A Polars DataFrame.
        resource_properties: The specific `ResourceProperties` for the `data`.

    Returns:
        Output the `data` if checks all pass.

    Raises:
        ExceptionGroup[CheckError]: If the resource properties are incorrect.
        ValueError: If column names in the data are incorrect.
        ExceptionGroup[ValueError]: If data types in the data are incorrect.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp

        sp.check_data(
            data=sp.example_data(),
            resource_properties=sp.example_resource_properties()
        )
        ```
    """
    check_resource_properties(resource_properties)
    _check_column_names(data, resource_properties)
    _check_column_types(data, resource_properties)
    # _check_column_values_constraints(data, resource_properties)

    return data


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


def _check_column_types(
    data: pl.DataFrame, resource_properties: ResourceProperties
) -> pl.DataFrame:
    """Checks that column data types match the data types specified in the properties.

    The resource properties specify a Frictionless data type for each column.
    This function checks if the Polars data type of each column in the data matches
    the expected Frictionless data type.

    Column names are expected to match the names specified in the resource properties.

    Args:
        data: The data frame to check.
        resource_properties: The resource properties to check against.

    Returns:
        The data frame, if all column types are correct.

    Raises:
        ExceptionGroup: A group of `ValueError`s, one per incorrectly typed column.
    """
    fields: list[FieldProperties] = get_nested_attr(
        resource_properties, "schema.fields", default=[]
    )
    polars_schema = data.schema
    errors = [
        _get_column_type_error(polars_schema[field.name], field)
        for field in fields
        if _not_allowed_type(polars_schema[field.name], field)
    ]

    if errors:
        raise ExceptionGroup(
            (
                "The following columns in the data have data types that do not match "
                "the data types in the resource properties:"
            ),
            errors,
        )
    return data


def _not_allowed_type(polars_type: pl.DataType, field: FieldProperties) -> bool:
    """Returns True if the Polars type does not match the Frictionless type.

    Args:
        polars_type: The Polars type.
        field: The field properties.

    Returns:
        True if the Polars type does not match the Frictionless type, False otherwise.
    """
    is_allowed_type = _FRICTIONLESS_TO_POLARS_TYPE_CHECK[field.type or "any"]
    return not is_allowed_type(polars_type)


def _get_column_type_error(
    polars_type: pl.DataType, field: FieldProperties
) -> ValueError:
    """Creates an error for a column where Polars and Frictionless types don't match.

    Args:
        polars_type: The Polars type.
        field: The field properties.

    Returns:
        A `ValueError`.
    """
    allowed_types = _FRICTIONLESS_TO_ALLOWED_POLARS_TYPES[field.type or "any"]
    return ValueError(
        f"Expected type of column '{field.name}' "
        f"to be {allowed_types} but found '{polars_type}'."
    )


# Mapping from Frictionless types to check functions for allowed Polars types
_FRICTIONLESS_TO_POLARS_TYPE_CHECK: dict[FieldType, Callable[[pl.DataType], bool]] = {
    "string": lambda dtype: isinstance(dtype, (pl.String, pl.Categorical, pl.Enum)),
    "integer": lambda dtype: dtype.is_integer(),
    "number": lambda dtype: dtype.is_float() or dtype.is_decimal(),
    "year": lambda dtype: dtype.is_integer(),
    "geopoint": lambda dtype: (
        isinstance(dtype, pl.Array) and dtype.size == 2 and dtype.inner.is_numeric()
    ),
    "datetime": lambda dtype: dtype == pl.Datetime,
    "date": lambda dtype: dtype == pl.Date,
    "time": lambda dtype: dtype == pl.Time,
    "yearmonth": lambda dtype: dtype == pl.Date,
    "boolean": lambda dtype: dtype == pl.Boolean,
    "duration": lambda dtype: dtype == pl.String,
    "object": lambda dtype: dtype == pl.String,
    "array": lambda dtype: dtype == pl.String,
    "geojson": lambda dtype: dtype == pl.String,
    "any": lambda _: True,
}

# Mapping from Frictionless types to descriptions of allowed Polars types
_FRICTIONLESS_TO_ALLOWED_POLARS_TYPES: dict[FieldType, str] = {
    "string": "a string, categorical, or enum type",
    "integer": "an integer type",
    "number": "a float or decimal type",
    "year": "an integer type",
    "geopoint": "an array of a numeric type with size 2",
    "datetime": f"'{pl.Datetime}'",
    "date": f"'{pl.Date}'",
    "time": f"'{pl.Time}'",
    "yearmonth": f"'{pl.Date}'",
    "boolean": f"'{pl.Boolean}'",
    "duration": f"'{pl.String}'",
    "object": f"'{pl.String}'",
    "array": f"'{pl.String}'",
    "geojson": f"'{pl.String}'",
    "any": "any type",
}

import re
from pathlib import Path

import polars as pl
from pytest import fixture, raises

from seedcase_sprout.core.properties import (
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from seedcase_sprout.core.sprout_checks.check_data_types import check_data_types
from tests.core.sprout_checks.test_check_column_data_types import (
    ANY_VALUES,
    ARRAY_BAD_VALUES,
    ARRAY_GOOD_VALUES,
    BOOLEAN_BAD_VALUES,
    BOOLEAN_GOOD_VALUES,
    DATE_BAD_VALUES,
    DATE_GOOD_VALUES,
    DATETIME_BAD_VALUES_WHEN_NO_TIMEZONE,
    DATETIME_BAD_VALUES_WHEN_TIMEZONE,
    DATETIME_GOOD_VALUES_WHEN_NO_TIMEZONE,
    DATETIME_GOOD_VALUES_WHEN_TIMEZONE,
    DURATION_VALUES,
    GEOPOINT_BAD_VALUES,
    GEOPOINT_GOOD_VALUES,
    INTEGER_BAD_VALUES,
    INTEGER_GOOD_VALUES,
    NUMBER_BAD_VALUES,
    NUMBER_GOOD_VALUES,
    OBJECT_BAD_VALUES,
    OBJECT_GOOD_VALUES,
    STRING_VALUES,
    TIME_BAD_VALUES,
    TIME_GOOD_VALUES,
    YEARMONTH_BAD_VALUES,
    YEARMONTH_GOOD_VALUES,
)

resource_properties = ResourceProperties(
    name="data",
    title="data",
    path=str(Path("resources", "1", "data.csv")),
    description="My data...",
    schema=TableSchemaProperties(
        fields=[
            FieldProperties(name="my_string", type="string"),
            FieldProperties(name="my_any", type="any"),
            FieldProperties(name="my_none", type=None),
            FieldProperties(name="my_duration", type="duration"),
            FieldProperties(name="my_boolean", type="boolean"),
            FieldProperties(name="my_yearmonth", type="yearmonth"),
            FieldProperties(name="my_date", type="date"),
            FieldProperties(name="my_datetime_tz", type="datetime"),
            FieldProperties(name="my_datetime_no_tz", type="datetime"),
            FieldProperties(name="my_datetime_null_start", type="datetime"),
            FieldProperties(name="my_time", type="time"),
            FieldProperties(name="my_year", type="year"),
            FieldProperties(name="my_integer", type="integer"),
            FieldProperties(name="my_number", type="number"),
            FieldProperties(name="my_geopoint", type="geopoint"),
            FieldProperties(name="my_array", type="array"),
            FieldProperties(name="my_object", type="object"),
            FieldProperties(name="my_geojson", type="geojson"),
        ]
    ),
)

bad_data = {
    "my_boolean": BOOLEAN_BAD_VALUES,
    "my_yearmonth": YEARMONTH_BAD_VALUES,
    "my_date": DATE_BAD_VALUES,
    "my_time": TIME_BAD_VALUES,
    "my_integer": INTEGER_BAD_VALUES,
    "my_year": INTEGER_BAD_VALUES,
    "my_number": NUMBER_BAD_VALUES,
    "my_geopoint": GEOPOINT_BAD_VALUES,
    "my_array": ARRAY_BAD_VALUES,
    "my_object": OBJECT_BAD_VALUES,
    "my_geojson": OBJECT_BAD_VALUES,
    "my_datetime_tz": DATETIME_BAD_VALUES_WHEN_TIMEZONE,
    "my_datetime_no_tz": DATETIME_BAD_VALUES_WHEN_NO_TIMEZONE,
    "my_datetime_null_start": DATETIME_BAD_VALUES_WHEN_NO_TIMEZONE,
}


@fixture
def data():
    data = {
        "my_boolean": BOOLEAN_GOOD_VALUES,
        "my_integer": INTEGER_GOOD_VALUES,
        "my_number": NUMBER_GOOD_VALUES,
        "my_year": INTEGER_GOOD_VALUES,
        "my_yearmonth": YEARMONTH_GOOD_VALUES,
        "my_datetime_tz": DATETIME_GOOD_VALUES_WHEN_TIMEZONE,
        "my_datetime_no_tz": DATETIME_GOOD_VALUES_WHEN_NO_TIMEZONE,
        "my_datetime_null_start": [None] + DATETIME_GOOD_VALUES_WHEN_NO_TIMEZONE,
        "my_date": DATE_GOOD_VALUES,
        "my_time": TIME_GOOD_VALUES,
        "my_geopoint": GEOPOINT_GOOD_VALUES,
        "my_array": ARRAY_GOOD_VALUES,
        "my_object": OBJECT_GOOD_VALUES,
        "my_geojson": OBJECT_GOOD_VALUES,
        "my_string": STRING_VALUES,
        "my_duration": DURATION_VALUES,
        "my_any": ANY_VALUES,
        "my_none": ANY_VALUES,
    }

    # Make all columns have the same number of rows
    # Add at least one null in each column
    max_rows = max(len(column) for column in data.values())
    return {
        col_name: column + [None] * (max_rows - len(column) + 1)
        for col_name, column in data.items()
    }


def test_no_error_raised_when_properties_empty(data):
    """Should raise no errors when the properties are empty."""
    df = pl.DataFrame(data, strict=False)

    assert check_data_types(df, ResourceProperties()) is df


def test_no_error_raised_when_data_types_match_properties(data):
    """When the data frame only contains correct data, no error is raised."""
    df = pl.DataFrame(data, strict=False)

    assert check_data_types(df, resource_properties) is df


def test_error_raised_when_data_types_do_not_match_properties(data):
    """When the data frame contains incorrect data, an error is raised for each column
    with incorrect values. Each error's error message lists the row indices of the
    incorrect values and the incorrect values themselves."""
    # Replace last 3 good values with bad values in each (non-string) column
    for col_name, column in data.items():
        if col_name in bad_data:
            column[-3:] = bad_data[col_name][:3]
    bad_rows = range(len(next(iter(data.values()))))[-3:]
    df = pl.DataFrame(data, strict=False)

    with raises(ExceptionGroup) as error_info:
        check_data_types(df, resource_properties)

    errors = error_info.value.exceptions

    # One error for each column with incorrect values
    assert len(errors) == len(bad_data)

    # Each column should have the incorrect values listed in the corresponding error
    for col_name, column in bad_data.items():
        error_message = next(
            str(error) for error in errors if f"'{col_name}'" in str(error)
        )
        # Find all incorrect values, e.g. [11]: 'not a date'
        flagged_values = re.findall(r"\[(\d+)\]: '([^']*)'", error_message)
        expected_flagged_values = [
            (str(row), str(value)) for row, value in zip(bad_rows, column[:3])
        ]
        assert f"column '{col_name}'" in error_message
        assert flagged_values == expected_flagged_values

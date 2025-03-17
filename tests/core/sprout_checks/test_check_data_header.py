from pathlib import Path

import polars as pl
from pytest import fixture, mark, raises

from seedcase_sprout.core.properties import (
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from seedcase_sprout.core.sprout_checks.check_data_header import check_data_header

string_field = FieldProperties(name="my_string", type="string")
date_field = FieldProperties(name="my_date", type="date")
number_field = FieldProperties(name="my_number", type="number")


@fixture
def resource_properties() -> ResourceProperties:
    return ResourceProperties(
        name="data",
        title="data",
        path=str(Path("resources", "1", "data.csv")),
        description="My data...",
        schema=TableSchemaProperties(),
    )


def test_no_error_when_data_frame_and_properties_both_empty():
    """Should throw no error if the data frame and the properties are both empty."""
    df = pl.DataFrame({})

    assert check_data_header(df, ResourceProperties()) is df


def test_no_error_when_data_column_names_match_properties(resource_properties):
    """Should throw no error if the column names in the data frame match the column
    names in the properties."""
    df = pl.DataFrame(
        {
            string_field.name: ["abc", "def"],
            date_field.name: ["2020-12-03", "2029-09-09"],
            number_field.name: [23, 45],
        }
    )
    resource_properties.schema.fields = [string_field, date_field, number_field]

    assert check_data_header(df, resource_properties) is df


@mark.parametrize(
    "data, fields",
    [
        ({"column": [123, 456]}, []),
        ({"wrong_name": ["value"]}, [string_field]),
        (
            {string_field.name: ["val"], date_field.name: ["1023-02-12"]},
            [date_field, string_field],
        ),
        ({date_field.name: ["2023-12-12"], "extra_name": ["val"]}, [date_field]),
        ({date_field.name: ["2012-12-12"]}, [date_field, string_field]),
        ({date_field.name: ["2012-12-12"], "": [""]}, [date_field, string_field]),
    ],
)
def test_throws_error_when_data_column_names_do_not_match_properties(
    data, fields, resource_properties
):
    """Should throw an error if the column names in the data frame don't match the
    column names in the properties."""
    df = pl.DataFrame(data)
    resource_properties.schema.fields = fields

    with raises(ValueError):
        check_data_header(df, resource_properties)

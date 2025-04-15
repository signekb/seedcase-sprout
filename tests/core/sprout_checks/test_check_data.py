import re
from pathlib import Path

import polars as pl
from polars.testing import assert_frame_equal
from pytest import fixture, mark, raises

from seedcase_sprout.core.check_data import (
    _FRICTIONLESS_TO_ALLOWED_POLARS_TYPES,
    check_data,
)
from seedcase_sprout.core.examples import (
    example_data,
    example_data_all_types,
    example_resource_properties,
    example_resource_properties_all_types,
)
from seedcase_sprout.core.properties import (
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from tests.core.assert_raises_errors import (
    assert_raises_check_errors,
    assert_raises_errors,
)

string_field = FieldProperties(name="my_string", type="string")
bool_field = FieldProperties(name="my_bool", type="boolean")
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


def test_accepts_correct_columns():
    """Should not raise an error when columns in the data match columns in the
    resource properties."""
    resource_properties = example_resource_properties_all_types()
    resource_properties.schema.fields += [
        FieldProperties(name="my_categorical", type="string"),
        FieldProperties(name="my_enum", type="string"),
        FieldProperties(name="my_int8", type="integer"),
        FieldProperties(name="my_int8_year", type="year"),
        FieldProperties(name="my_uint64", type="integer"),
        FieldProperties(name="my_float32", type="number"),
        FieldProperties(name="my_decimal", type="number"),
        FieldProperties(name="my_int_geopoint", type="geopoint"),
    ]
    data = example_data_all_types().with_columns(
        [
            pl.Series(
                "my_categorical", ["low", "medium", "high"], dtype=pl.Categorical
            ),
            pl.Series(
                "my_enum",
                ["low", "low", "high"],
                dtype=pl.Enum(["low", "medium", "high"]),
            ),
            pl.Series("my_int8", [1, 22, 33], dtype=pl.Int8),
            pl.Series("my_int8_year", [1, 22, 33], dtype=pl.Int8),
            pl.Series("my_uint64", [1, 22, 33], dtype=pl.UInt64),
            pl.Series("my_float32", [1.1, 2.2, 3.3], dtype=pl.Float32),
            pl.Series("my_decimal", ["1.20", "2.56", "3.39"], dtype=pl.Decimal),
            pl.Series(
                "my_int_geopoint",
                [[3, 4], [5, 45], [12, -4]],
                dtype=pl.Array(pl.Int16, 2),
            ),
        ]
    )

    assert_frame_equal(check_data(data, resource_properties), data)


def test_accepts_columns_in_any_order():
    """Should not raise an error when the data types match but the columns are in a
    different order."""
    resource_properties = example_resource_properties()
    resource_properties.schema.fields.reverse()
    data = example_data()

    assert_frame_equal(check_data(data, resource_properties), data)


def test_throws_error_when_data_has_extra_columns(resource_properties):
    """Should throw an error if the data has extra columns."""
    df = pl.DataFrame({"extra_col1": [""], bool_field.name: [True], "extra_col2": [""]})
    resource_properties.schema.fields = [bool_field]

    with raises(ValueError, match=r"Unexpected.*extra_col1.*extra_col2") as error:
        check_data(df, resource_properties)

    assert bool_field.name not in str(error)


def test_throws_error_when_data_has_missing_columns(resource_properties):
    """Should throw an error if the data has missing columns."""
    df = pl.DataFrame({bool_field.name: [True]})
    resource_properties.schema.fields = [string_field, bool_field, number_field]

    with raises(
        ValueError, match=rf"Missing.*{string_field.name}.*{number_field.name}"
    ) as error:
        check_data(df, resource_properties)

    assert bool_field.name not in str(error)


def test_throws_error_when_data_has_extra_and_missing_columns(resource_properties):
    """Should throw an error if the data has extra columns and missing columns."""
    df = pl.DataFrame({"extra_col": [""], bool_field.name: [True]})
    resource_properties.schema.fields = [string_field, bool_field, number_field]

    with raises(ValueError) as error:
        check_data(df, resource_properties)

    assert re.search(r"Unexpected.*extra_col", str(error))
    assert re.search(rf"Missing.*{string_field.name}.*{number_field.name}", str(error))
    assert bool_field.name not in str(error)


@mark.parametrize(
    "frictionless_type",
    [
        "string",
        "boolean",
        "integer",
        "number",
        "year",
        "datetime",
        "date",
        "time",
        "yearmonth",
        "geopoint",
        "duration",
        "object",
        "array",
        "geojson",
    ],
)
def test_rejects_incorrect_column_type(frictionless_type):
    """Should raise an error if the Polars type does not match the Frictionless type."""
    data = pl.DataFrame({"my_col": pl.Series([{"prop": "value"}] * 3, dtype=pl.Object)})
    resource_properties = example_resource_properties()
    resource_properties.schema.fields = [
        FieldProperties(name="my_col", type=frictionless_type)
    ]

    with raises(ExceptionGroup) as error_info:
        check_data(data, resource_properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    polars_type = re.escape(str(data.schema.dtypes()[0]))
    allowed_types = _FRICTIONLESS_TO_ALLOWED_POLARS_TYPES[frictionless_type]
    assert re.search(
        rf"'my_col'.*{allowed_types}.*found '{polars_type}'", str(errors[0])
    )


def test_rejects_multiple_incorrect_column_types():
    """Should raise an error if multiple column types don't match."""
    resource_properties = example_resource_properties()
    data = example_data()
    data = data.select([pl.lit(None).alias(col) for col in data.columns])

    with raises(ExceptionGroup) as error_info:
        check_data(data, resource_properties)

    errors = error_info.value.exceptions
    assert len(errors) == data.width
    for error, field in zip(errors, resource_properties.schema.fields):
        polars_type = re.escape(str(data.schema[field.name]))
        allowed_types = _FRICTIONLESS_TO_ALLOWED_POLARS_TYPES[field.type]
        assert re.search(
            rf"'{field.name}'.*{allowed_types}.*found '{polars_type}'", str(error)
        )


def test_rejects_geopoint_with_incorrect_size():
    """Should raise an error if the size of the array representing a geopoint is not
    correct."""
    data = pl.DataFrame(
        {"my_geopoint": pl.Series([[1, 1, 1]] * 3, dtype=pl.Array(pl.Int8, 3))}
    )
    resource_properties = example_resource_properties()
    resource_properties.schema.fields = [
        FieldProperties(name="my_geopoint", type="geopoint")
    ]

    assert_raises_errors(lambda: check_data(data, resource_properties), ValueError, 1)


def test_rejects_geopoint_with_incorrect_inner_type():
    """Should raise an error if the type of the nested elements in a geopoint array is
    not correct."""
    data = pl.DataFrame(
        {"my_geopoint": pl.Series([["a", "b"]] * 3, dtype=pl.Array(pl.String, 2))}
    )
    resource_properties = example_resource_properties()
    resource_properties.schema.fields = [
        FieldProperties(name="my_geopoint", type="geopoint")
    ]

    assert_raises_errors(lambda: check_data(data, resource_properties), ValueError, 1)


def test_rejects_incorrect_resource_properties():
    """Should throw an error if the resource properties are incorrect."""
    assert_raises_check_errors(lambda: check_data(example_data(), ResourceProperties()))

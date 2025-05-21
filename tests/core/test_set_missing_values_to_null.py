import polars as pl
from polars.testing import assert_frame_equal
from pytest import fixture, mark

from seedcase_sprout.core.properties import (
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from seedcase_sprout.core.set_missing_values_to_null import set_missing_values_to_null

missing_values = ["None", "NA", "*", "some text", ""]


@fixture
def resource_properties() -> ResourceProperties:
    return ResourceProperties(
        name="data",
        title="data",
        description="My data...",
        schema=TableSchemaProperties(),
    )


def test_no_null_conversion_done_when_properties_empty():
    """No values should be set to null when the properties are empty."""
    df = pl.DataFrame({"my_string": missing_values})

    assert_frame_equal(set_missing_values_to_null(df, ResourceProperties()), df)


def test_sets_values_in_schema_missing_values_to_null(resource_properties):
    """Should convert values listed in `schema.missing_values` to null."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_date",
            type="date",
        )
    ]
    resource_properties.schema.missing_values = missing_values
    df = pl.DataFrame({"my_date": ["1212-09-08"] + missing_values})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_date").to_list() == ["1212-09-08"] + [None] * 5


def test_sets_values_in_field_missing_values_to_null(resource_properties):
    """Should convert values listed in `field.missing_values` to null."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_date",
            type="date",
            missing_values=missing_values,
        )
    ]
    df = pl.DataFrame({"my_date": ["1212-09-08"] + missing_values})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_date").to_list() == ["1212-09-08"] + [None] * 5


@mark.parametrize("schema_missing_values", [["schema-missing-value"], [], None])
def test_field_missing_values_override_schema_missing_values(
    resource_properties, schema_missing_values
):
    """If both `schema.missing_values` and `field.missing_values` are set, the latter
    takes precedence. Fields with a value in `schema.missing_values` are not changed to
    null."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_string",
            type="string",
            missing_values=["field-missing-value"],
        ),
    ]
    resource_properties.schema.missing_values = schema_missing_values
    df = pl.DataFrame(
        {"my_string": ["schema-missing-value", "some value", "", "field-missing-value"]}
    )

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_string").to_list() == [
        "schema-missing-value",
        "some value",
        "",
        None,
    ]


@mark.parametrize("schema_missing_values", [["schema-missing-value"], [], None])
def test_no_values_set_to_null_when_field_missing_values_empty(
    resource_properties, schema_missing_values
):
    """When `field.missing_values` is set to the empty list, no value counts as missing
    and no null conversion is done."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_string",
            type="string",
            missing_values=[],
        ),
    ]
    resource_properties.schema.missing_values = schema_missing_values
    df = pl.DataFrame({"my_string": ["schema-missing-value", "some value", ""]})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_string").to_list() == [
        "schema-missing-value",
        "some value",
        "",
    ]


def test_no_values_set_to_null_when_schema_missing_values_empty(resource_properties):
    """When `schema.missing_values` is set to the empty list and `field.missing_values`
    is not set, no value counts as missing and no null conversion is done."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_string",
            type="string",
        ),
    ]
    resource_properties.schema.missing_values = []
    df = pl.DataFrame({"my_string": ["None", "some value", ""]})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_string").to_list() == [
        "None",
        "some value",
        "",
    ]


def test_empty_string_set_to_null_by_default(resource_properties):
    """When missing values are not set, empty strings are set to null by default."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_string",
            type="string",
        ),
    ]
    df = pl.DataFrame({"my_string": ["None", "some value", ""]})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_string").to_list() == [
        "None",
        "some value",
        None,
    ]


def test_sets_value_to_null_only_if_full_match(resource_properties):
    """A value is set to null only if it fully matches one of the missing values."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="my_date",
            type="date",
        )
    ]
    resource_properties.schema.missing_values = ["11-11"]
    df = pl.DataFrame({"my_date": ["1234-11-11", "11-11", ""]})

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("my_date").to_list() == ["1234-11-11", None, ""]


def test_field_missing_values_can_be_set_separately_for_each_field(resource_properties):
    """`field.missing_values` can be set separately for each field."""
    resource_properties.schema.fields = [
        FieldProperties(
            name="col1",
            type="date",
            missing_values=["field-1-missing"],
        ),
        FieldProperties(
            name="col2",
            type="date",
            missing_values=["field-2-missing"],
        ),
    ]
    df = pl.DataFrame(
        {
            "col1": ["field-1-missing", "1234-11-11"],
            "col2": ["1010-09-08", "field-2-missing"],
        }
    )

    df_with_nulls = set_missing_values_to_null(df, resource_properties)

    assert df_with_nulls.get_column("col1").to_list() == [None, "1234-11-11"]
    assert df_with_nulls.get_column("col2").to_list() == ["1010-09-08", None]

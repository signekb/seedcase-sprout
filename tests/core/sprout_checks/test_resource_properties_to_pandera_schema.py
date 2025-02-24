import polars as pl
from pytest import mark

from seedcase_sprout.core.properties import (
    ConstraintsProperties,
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from seedcase_sprout.core.sprout_checks.resource_properties_to_pandera_schema import (
    resource_properties_to_pandera_schema,
)


@mark.parametrize(
    "resource_properties",
    [
        ResourceProperties(),
        ResourceProperties(
            schema=TableSchemaProperties(),
        ),
        ResourceProperties(
            schema=TableSchemaProperties(fields=None),
        ),
        ResourceProperties(
            schema=TableSchemaProperties(fields=[]),
        ),
    ],
)
def test_converts_properties_without_fields(resource_properties):
    """When the properties have no fields, the Pandera schema should have no columns."""
    schema = resource_properties_to_pandera_schema(resource_properties)

    assert schema.columns == {}
    assert schema.strict


@mark.parametrize(
    "field_type,data_type,num_checks",
    [
        ("number", pl.Float64, 0),
        ("integer", pl.Int64, 0),
        ("string", pl.String, 0),
        ("boolean", pl.String, 1),
        ("object", pl.String, 1),
        ("array", pl.String, 1),
        ("list", pl.String, 0),
        ("datetime", pl.String, 1),
        ("date", pl.String, 1),
        ("time", pl.String, 1),
        ("year", pl.String, 1),
        ("yearmonth", pl.String, 1),
        ("duration", pl.String, 1),
        ("geopoint", pl.String, 1),
        ("any", pl.String, 0),
        (None, pl.String, 0),
    ],
)
def test_converts_individual_fields_correctly(field_type, data_type, num_checks):
    """Should convert each type of field to a Pandera column correctly."""
    resource_properties = ResourceProperties(
        schema=TableSchemaProperties(
            fields=[FieldProperties(name="my_field", type=field_type)]
        )
    )

    schema = resource_properties_to_pandera_schema(resource_properties)

    assert schema.strict
    assert len(schema.columns) == 1
    column = list(schema.columns.values())[0]
    assert column.name == "my_field"
    assert column.dtype.type == data_type
    assert len(column.checks) == num_checks
    assert column.coerce
    assert column.nullable
    assert column.required


def test_converts_multiple_fields():
    """Should convert multiple fields to multiple Pandera columns correctly."""
    resource_properties = ResourceProperties(
        schema=TableSchemaProperties(
            fields=[
                FieldProperties(name="my_date", type="date"),
                FieldProperties(name="my_boolean", type="boolean"),
            ]
        )
    )

    schema = resource_properties_to_pandera_schema(resource_properties)

    assert [(column.name, column.dtype.type) for column in schema.columns.values()] == [
        ("my_date", pl.String),
        ("my_boolean", pl.String),
    ]


@mark.parametrize("required,expected", [(True, False), (False, True), (None, True)])
def test_converts_required_constraint(required, expected):
    """Should convert the required constraint to Pandera's nullable correctly."""
    resource_properties = ResourceProperties(
        schema=TableSchemaProperties(
            fields=[
                FieldProperties(
                    name="my_date",
                    type="date",
                    constraints=ConstraintsProperties(required=required),
                )
            ]
        )
    )

    schema = resource_properties_to_pandera_schema(resource_properties)

    column = list(schema.columns.values())[0]
    assert column.nullable is expected

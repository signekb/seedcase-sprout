from pathlib import Path

from pytest import fixture, mark, raises

from seedcase_sprout.core.not_properties_error import NotPropertiesError
from seedcase_sprout.core.properties import ResourceProperties, TableSchemaProperties
from seedcase_sprout.core.verify_resource_properties import (
    REQUIRED_RESOURCE_PROPERTIES,
    verify_resource_properties,
)


@fixture
def resource_properties() -> dict:
    return ResourceProperties(
        name="my-resource",
        path=str(Path("resources", "1", "data.parquet")),
        title="My Resource",
        description="This is my resource.",
    ).compact_dict


def test_accepts_required_fields(resource_properties):
    """Should accept an object containing values for required fields."""
    assert verify_resource_properties(resource_properties) == resource_properties


def test_accepts_required_and_optional_fields(resource_properties):
    """Should accept an object containing values for required and optional fields."""
    resource_properties["format"] = "csv"
    resource_properties["mediatype"] = "image/png"
    resource_properties["bytes"] = 5678
    resource_properties["custom"] = 123

    assert verify_resource_properties(resource_properties) == resource_properties


def test_accepts_properties_with_only_schema_error(resource_properties):
    """Should not throw if there's a malformed schema but the resource properties are
    correct."""
    bad_schema = TableSchemaProperties(fields="these are not fields").compact_dict
    resource_properties["schema"] = bad_schema

    assert verify_resource_properties(resource_properties) == resource_properties


def test_rejects_empty_object():
    """Should reject an empty object."""
    with raises(NotPropertiesError) as error:
        verify_resource_properties({})

    message = str(error.value)
    for field in REQUIRED_RESOURCE_PROPERTIES:
        assert f"'{field}' is a required property" in message


def test_rejects_properties_violating_spec(resource_properties):
    """Should reject an object with a value not meeting the Data Package spec."""
    resource_properties["name"] = "an invalid name"

    with raises(NotPropertiesError, match="at property 'name'"):
        verify_resource_properties(resource_properties)


@mark.parametrize("field", REQUIRED_RESOURCE_PROPERTIES)
@mark.parametrize("empty_value", ["", None])
def test_rejects_empty_value_for_required_fields(
    resource_properties, field, empty_value
):
    """Should reject an object with a missing or blank required field."""
    resource_properties[field] = empty_value

    with raises(NotPropertiesError, match=f"'{field}' is a required property"):
        verify_resource_properties(resource_properties)


@mark.parametrize(
    "data_path",
    [
        Path("resources", "x", "data.parquet"),
        Path("1", "data.parquet"),
        Path("resources", "1", "data.parquet", "1"),
    ],
)
def test_rejects_malformed_path(resource_properties, data_path):
    """Given a set of properties with a malformed data path, should throw
    NotPropertiesError."""
    resource_properties["path"] = str(data_path)

    with raises(
        NotPropertiesError,
        match="No resource ID found",
    ):
        verify_resource_properties(resource_properties)

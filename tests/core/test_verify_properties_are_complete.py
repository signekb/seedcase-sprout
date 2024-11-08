from frictionless.errors import PackageError
from pytest import mark, raises

from seedcase_sprout.core.not_properties_error import NotPropertiesError
from seedcase_sprout.core.verify_properties_are_complete import (
    verify_properties_are_complete,
)


@mark.parametrize("required_fields", [{}, {"field1"}, {"field1", "field2"}])
def test_accepts_required_fields(required_fields):
    """Should accept an object containing values for all required fields."""
    properties = {
        "field1": "my field 1",
        "field2": "my field 2",
        "field3": "my field 3",
        "field4": "",
    }

    assert (
        verify_properties_are_complete(properties, PackageError, required_fields)
        == properties
    )


def test_rejects_empty_object():
    """Should reject an empty object."""
    required_fields = {"field1", "field2"}

    with raises(NotPropertiesError) as error:
        verify_properties_are_complete({}, PackageError, required_fields)

    message = str(error.value)
    for field in required_fields:
        assert f"'{field}' is a required property" in message


@mark.parametrize("empty_value", ["", None])
def test_rejects_empty_value_for_required_fields(empty_value):
    """Should reject an object with a missing or blank required field."""
    properties = {
        "field1": empty_value,
    }

    with raises(NotPropertiesError, match="'field1' is a required property"):
        verify_properties_are_complete(properties, PackageError, {"field1"})

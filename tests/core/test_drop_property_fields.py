from pytest import mark

from sprout.core.drop_property_fields import drop_property_fields


def test_drops_one_field():
    """Given a single existing field to drop, should return the input
    without that field."""
    properties = {"test1": "value1", "test2": "value2"}
    expected_properties = {"test2": "value2"}

    assert drop_property_fields(properties, ["test1"]) == expected_properties


def test_drops_multiple_fields():
    """Given multiple existing fields to drop, should return the input
    without those fields."""
    properties = {
        "test1": "value1",
        "test2": "value2",
        "test3": "value3",
    }
    expected_properties = {"test3": "value3"}

    assert drop_property_fields(properties, ["test1", "test2"]) == expected_properties


def test_drops_no_fields_if_input_empty():
    """Given an empty list of fields, should return the input without changing it."""
    properties = {"test1": "value1"}
    assert drop_property_fields(properties, []) == properties


@mark.parametrize("properties", [{}, {"test1": "value1"}])
def test_ignores_nonexistent_field(properties):
    """Given a nonexistent field to drop, should return the input
    without changing it."""
    assert drop_property_fields(properties, ["nonexistent"]) == properties

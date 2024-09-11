from pytest import mark, raises

from sprout.core.edit_property_field import edit_property_field


@mark.parametrize(
    "value", ["new value", 123, [1, 2, 3], {"outer": {"inner": "new value"}}]
)
def test_updates_existing_property(value):
    """Given a properties object with the specified property, should update that
    property to the specified value."""
    properties = {"test": "old value"}
    expected_properties = {"test": value}
    assert edit_property_field(properties, "test", value) == expected_properties


def test_rejects_nonexistent_property():
    """Given a properties object without the specified property, should raise
    KeyError."""
    properties = {"test": "old value"}
    with raises(KeyError):
        edit_property_field(properties, "nonexistent", "new value")

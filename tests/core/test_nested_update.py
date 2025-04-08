from seedcase_sprout.core.nested_update import nested_update
from seedcase_sprout.core.properties import (
    FieldProperties,
    ResourceProperties,
    TableSchemaProperties,
)


def test_original_dictionaries_not_modified():
    """The original dictionaries should not be modified by the update."""
    old = {"level1": {"level2": {"prop1": "old"}}}
    updates = {"level1": {"level2": {"prop1": "new"}}}

    nested_update(old, updates)

    assert old == {"level1": {"level2": {"prop1": "old"}}}
    assert updates == {"level1": {"level2": {"prop1": "new"}}}


def test_merges_nested_dictionaries():
    """Dictionaries should be updated using the 'merge' strategy. Unchanged values
    should not be overwritten."""
    old = {"level1": {"level2": {"prop1": "a", "prop2": "b"}}}
    updates = {"level1": {"level2": {"prop1": "new"}}}

    assert nested_update(old, updates) == {
        "level1": {"level2": {"prop1": "new", "prop2": "b"}}
    }


def test_overrides_lists():
    """Lists should be updated using the 'override' strategy."""
    old = {"level1": {"level2": [{"prop1": "a", "prop2": "b"}]}}
    updates = {"level1": {"level2": [{"prop1": "new"}]}}

    assert nested_update(old, updates) == {"level1": {"level2": [{"prop1": "new"}]}}


def test_overrides_other_types():
    """Non-listed types should be updated using the 'override' strategy."""
    old = {"level1": {"level2": ({"prop1": "a"}, {"prop2": "b"})}}
    updates = {"level1": {"level2": ({"prop1": "new"},)}}

    assert nested_update(old, updates) == {"level1": {"level2": ({"prop1": "new"},)}}


def test_overrides_conflicting_types():
    """Conflicting types should be updated using the 'override' strategy."""
    old = {"level1": {"level2": {"prop1": "a", "prop2": "b"}}}
    updates = {"level1": {"level2": [{"prop1": "new"}]}}

    assert nested_update(old, updates) == {"level1": {"level2": [{"prop1": "new"}]}}


def test_updating_properties_preserves_unchanged_values():
    """Updating properties should preserve unchanged values."""
    old = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields_match="equal",
            primary_key="id",
        ),
    )
    updates = ResourceProperties(
        schema=TableSchemaProperties(primary_key="code"),
    )
    expected = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields_match="equal",
            primary_key="code",
        ),
    )

    assert nested_update(old, updates) == expected


def test_updating_properties_overrides_lists():
    """When updating properties, lists should be overridden."""
    old = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields=[FieldProperties(name="my_old_field")],
            fields_match="equal",
        ),
    )
    updates = ResourceProperties(
        schema=TableSchemaProperties(fields=[FieldProperties(name="my_new_field")]),
    )
    expected = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields=[FieldProperties(name="my_new_field")],
            fields_match="equal",
        ),
    )

    assert nested_update(old, updates) == expected


def test_updating_properties_overrides_conflicting_types():
    """When updating properties, conflicting types should be overridden."""
    old = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields=[FieldProperties(name="id"), FieldProperties(name="code")],
            primary_key="id",
        ),
    )
    updates = ResourceProperties(
        schema=TableSchemaProperties(primary_key=["id", "code"]),
    )
    expected = ResourceProperties(
        name="old-name",
        title="Old Title",
        schema=TableSchemaProperties(
            fields=[FieldProperties(name="id"), FieldProperties(name="code")],
            primary_key=["id", "code"],
        ),
    )

    assert nested_update(old, updates) == expected

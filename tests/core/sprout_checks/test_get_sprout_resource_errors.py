from pathlib import Path

from pytest import fixture, mark

from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.sprout_checks.get_blank_value_for_type import (
    get_blank_value_for_type,
)
from seedcase_sprout.core.sprout_checks.get_json_path_to_resource_field import (
    get_json_path_to_resource_field,
)
from seedcase_sprout.core.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)
from seedcase_sprout.core.sprout_checks.required_fields import (
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)


@fixture
def properties():
    return ResourceProperties(
        name="resource-1",
        path=str(Path("resources", "1", "data.parquet")),
        title="Resource 1",
        description="A resource.",
    ).compact_dict


@fixture
def properties_partial():
    return ResourceProperties(
        path=str(Path("resources", "1", "data.parquet")),
    ).compact_dict


def test_passes_full_resource_properties(properties):
    """Should pass with a full set of resource properties."""
    assert get_sprout_resource_errors(properties) == []


@mark.parametrize("index", [None, 2])
def test_error_found_if_inline_data_is_set(properties, index):
    """Should find an error if inline data is set."""
    properties["data"] = "some data"

    errors = get_sprout_resource_errors(properties, index=index)

    assert len(errors) == 1
    assert errors[0].json_path == get_json_path_to_resource_field("data", index)
    assert errors[0].validator == "inline-data"


@mark.parametrize("index", [None, 2])
@mark.parametrize("name,type", RESOURCE_SPROUT_REQUIRED_FIELDS.items())
def test_error_found_if_fields_are_blank(properties, name, type, index):
    """Should find an error if there is one required field that is present but blank."""
    properties[name] = get_blank_value_for_type(type)

    errors = get_sprout_resource_errors(properties, index=index)
    blank_errors = [error for error in errors if error.validator == "blank"]

    assert len(blank_errors) == 1
    assert blank_errors[0].json_path == get_json_path_to_resource_field(name, index)


@mark.parametrize("index", [None, 2])
@mark.parametrize("name", RESOURCE_SPROUT_REQUIRED_FIELDS.keys())
def test_error_found_if_required_fields_are_missing(properties, name, index):
    """Should find an error if there is a missing required field."""
    del properties[name]

    errors = get_sprout_resource_errors(properties, index=index)
    required_errors = [error for error in errors if error.validator == "required"]

    assert len(required_errors) == 1
    assert required_errors[0].json_path == get_json_path_to_resource_field(name, index)


@mark.parametrize("path", ["", [], str(Path("resources", "1"))])
def test_error_found_if_data_path_is_incorrect_(properties, path):
    """Should find at least one error if `path` contains no resource ID, is not a
    string, or is otherwise malformed."""
    properties["path"] = path

    errors = get_sprout_resource_errors(properties)

    assert len(errors) >= 1

from dataclasses import replace
from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.core.create_resource_properties import create_resource_properties
from seedcase_sprout.core.properties import ResourceProperties


@fixture
def resource_properties() -> ResourceProperties:
    return ResourceProperties(
        name="resource-name",
        title="My Resource",
        description="Very interesting...",
    )


@fixture
def resource_path(tmp_path) -> Path:
    resource_path = tmp_path / "resources" / "1"
    resource_path.mkdir(parents=True)
    return resource_path


def test_creates_properties_with_required_fields_present(
    resource_properties, resource_path
):
    """Given properties with all required fields present (except `path`), it should
    create a set of resource properties with the correct `path`."""
    expected_properties = replace(
        resource_properties, path=str(Path("resources", "1", "data.parquet"))
    )

    assert (
        create_resource_properties(resource_properties, resource_path)
        == expected_properties
    )


def test_rejects_path_if_not_directory(tmp_path, resource_properties):
    """Given a path that is not a directory, should raise `NotADirectoryError`."""
    resource_path = tmp_path / "nonexistent"

    with raises(NotADirectoryError):
        create_resource_properties(resource_properties, resource_path)


def test_rejects_properties_if_incorrect_path_generated(tmp_path, resource_properties):
    """Should raise a `CheckError` if the `path` was not generated correctly."""
    with raises(ExceptionGroup) as error_info:
        create_resource_properties(resource_properties, tmp_path)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].validator == "pattern"
    assert errors[0].json_path == "$.path"


def test_rejects_properties_with_missing_required_fields(resource_path):
    """Given an empty properties input, should raise `CheckError`s."""
    with raises(ExceptionGroup) as error_info:
        create_resource_properties(ResourceProperties(), resource_path)

    errors = error_info.value.exceptions
    assert len(errors) == 3
    assert all(error.validator == "required" for error in errors)


def test_rejects_properties_with_an_incorrect_field(resource_properties, resource_path):
    """Should raise a `CheckError` if `name` doesn't match the pattern."""
    resource_properties.name = "invalid name with spaces"

    with raises(ExceptionGroup) as error_info:
        create_resource_properties(resource_properties, resource_path)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].validator == "pattern"
    assert errors[0].json_path == "$.name"


def test_defaults_to_cwd_if_no_path_provided(
    resource_properties, tmp_cwd, resource_path
):
    """Should locate resource in cwd if no path provided."""
    resource_properties.name = "1"
    expected_properties = replace(
        resource_properties, path=str(Path("resources", "1", "data.parquet"))
    )

    assert create_resource_properties(resource_properties) == expected_properties

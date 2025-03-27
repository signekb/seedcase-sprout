from json import JSONDecodeError
from pathlib import Path

from pytest import mark, raises

from seedcase_sprout.core import (
    ResourceProperties,
    example_package_properties,
    read_properties,
    write_package_properties,
)
from seedcase_sprout.core.sprout_checks.required_fields import (
    PACKAGE_SPROUT_REQUIRED_FIELDS,
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)
from seedcase_sprout.core.write_json import write_json


def test_reads_in_as_package_properties(tmp_path):
    """Should read in the properties from the `datapackage.json` file."""

    expected_properties = example_package_properties()
    properties_path = tmp_path / "datapackage.json"
    properties_path = write_package_properties(expected_properties, properties_path)
    actual_properties = read_properties(properties_path)

    assert expected_properties == actual_properties


def test_reads_when_resource_not_exists(tmp_path):
    """Should not give an error if there are no resources on the package."""

    expected_properties = example_package_properties()
    expected_properties.resources = None
    properties_path = tmp_path / "datapackage.json"
    properties_path = write_package_properties(expected_properties, properties_path)
    actual_properties = read_properties(properties_path)

    assert expected_properties == actual_properties


def test_throws_error_if_path_points_to_dir(tmp_path):
    """Should throw FileNotFoundError if the path points to a folder."""
    with raises(FileNotFoundError):
        read_properties(tmp_path)


def test_throws_error_if_path_points_to_nonexistent_file(tmp_path):
    """Should throw FileNotFoundError if the path points to a nonexistent file."""
    with raises(FileNotFoundError):
        read_properties(tmp_path / "datapackage.json")


def test_throws_error_if_properties_file_cannot_be_read(tmp_path):
    """Should throw JSONDecodeError if the properties file cannot be read as JSON."""
    file_path = Path(tmp_path / "datapackage.json")
    file_path.write_text(",,, this is not, JSON")

    with raises(JSONDecodeError):
        read_properties(file_path)


@mark.parametrize("field", [*PACKAGE_SPROUT_REQUIRED_FIELDS.keys()])
def test_raises_error_if_file_is_missing_required_field(field, tmp_path):
    """Should raise an error if a required field is missing from the file."""
    properties = example_package_properties()
    package_path = tmp_path / "datapackage.json"
    delattr(properties, field)
    write_json(properties.compact_dict, package_path)

    with raises(ExceptionGroup) as error_info:
        read_properties(package_path)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == f"$.{field}"
    assert errors[0].validator == "required"


@mark.parametrize("field", RESOURCE_SPROUT_REQUIRED_FIELDS.keys())
def test_raises_error_if_file_is_missing_required_resource_fields(field, tmp_path):
    """Should raise an error if a required resource field is missing from the file."""
    properties = example_package_properties()
    properties.resources = [
        ResourceProperties(
            name="resource-1",
            path=str(Path("resources", "1", "data.parquet")),
            title="Resource 1",
            description="A resource.",
        ),
        ResourceProperties(
            name="resource-2",
            path=str(Path("resources", "2", "data.parquet")),
            title="Resource 2",
            description="A second resource.",
        ),
    ]
    package_path = tmp_path / "datapackage.json"
    delattr(properties.resources[0], field)
    write_json(properties.compact_dict, package_path)

    with raises(ExceptionGroup) as error_info:
        read_properties(package_path)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == f"$.resources[0].{field}"
    assert errors[0].validator == "required"

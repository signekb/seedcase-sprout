from json import JSONDecodeError
from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.core.create_package_structure import create_package_structure
from seedcase_sprout.core.edit_package_properties import edit_package_properties
from seedcase_sprout.core.not_properties_error import NotPropertiesError
from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.write_json import write_json


@fixture
def properties():
    return PackageProperties(
        name="my-new-package-name",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="2.0.0",
        created="2024-05-14T05:00:01+00:00",
    )


@fixture
def properties_path(tmp_path) -> Path:
    properties_path = create_package_structure(tmp_path)[0]
    # Write a correct properties file to be edited
    write_json(
        PackageProperties(
            name="my-package",
            id="123-abc-123",
            title="My Package",
            description="This is my package.",
            version="1.0.0",
            created="2024-05-14T05:00:01+00:00",
            resources=[],
        ).compact_dict,
        properties_path,
    )
    return properties_path


def test_edits_only_changed_package_properties(properties_path, properties):
    """Should only edit package properties and leave unchanged values as is."""
    # Given
    current_properties = read_json(properties_path)

    # When, Then
    expected_properties = current_properties | properties.compact_dict
    assert edit_package_properties(
        properties_path, properties
    ) == PackageProperties.from_dict(expected_properties)


def test_throws_error_if_path_points_to_dir(tmp_path):
    """Should throw FileNotFoundError if the path points to a folder."""
    with raises(FileNotFoundError):
        edit_package_properties(tmp_path, PackageProperties())


def test_throws_error_if_path_points_to_nonexistent_file(tmp_path):
    """Should throw FileNotFoundError if the path points to a nonexistent file."""
    with raises(FileNotFoundError):
        edit_package_properties(tmp_path / "datapackage.json", PackageProperties())


def test_throws_error_if_properties_file_cannot_be_read(tmp_path, properties):
    """Should throw JSONDecodeError if the properties file cannot be read as JSON."""
    file_path = tmp_path / "datapackage.json"
    file_path.write_text(",,, this is not, JSON")

    with raises(JSONDecodeError):
        edit_package_properties(file_path, properties)


def test_throws_error_if_current_package_properties_are_malformed(tmp_path, properties):
    """Should throw NotPropertiesError if the current package properties are
    malformed."""
    package_properties = PackageProperties(name="invalid name with spaces").compact_dict
    path = write_json(package_properties, tmp_path / "datapackage.json")

    with raises(NotPropertiesError):
        edit_package_properties(path, properties)


def test_throws_error_if_new_properties_are_empty(properties_path):
    """Should throw NotPropertiesError if the new properties are empty."""
    with raises(NotPropertiesError):
        edit_package_properties(properties_path, PackageProperties())

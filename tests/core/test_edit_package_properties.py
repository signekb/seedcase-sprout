from json import JSONDecodeError
from pathlib import Path

from pytest import fixture, raises

from sprout.core.edit_package_properties import edit_package_properties
from sprout.core.not_properties_error import NotPropertiesError
from sprout.core.properties import PackageProperties
from sprout.core.write_json import write_json


@fixture
def properties():
    return PackageProperties(
        name="my-new-package-name",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="2.0.0",
        created="2024-05-14T05:00:01+00:00",
    ).asdict


@fixture
def properties_path(tmp_path) -> Path:
    package_properties = PackageProperties(version="1.0.0")
    return write_json(package_properties.asdict, tmp_path / "datapackage.json")


def test_edits_package_properties(properties_path, properties):
    """Should update package properties."""
    assert edit_package_properties(properties_path, properties) == properties


def test_throws_error_if_path_points_to_dir(tmp_path):
    """Should throw FileNotFoundError if the path points to a folder."""
    with raises(FileNotFoundError):
        edit_package_properties(tmp_path, {})


def test_throws_error_if_path_points_to_nonexistent_file(tmp_path):
    """Should throw FileNotFoundError if the path points to a nonexistent file."""
    with raises(FileNotFoundError):
        edit_package_properties(tmp_path / "datapackage.json", {})


def test_throws_error_if_properties_file_cannot_be_read(tmp_path, properties):
    """Should throw JSONDecodeError if the properties file cannot be read as JSON."""
    file_path = tmp_path / "datapackage.json"
    file_path.write_text(",,, this is not, JSON")

    with raises(JSONDecodeError):
        edit_package_properties(file_path, properties)


def test_throws_error_if_current_package_properties_are_malformed(tmp_path, properties):
    """Should throw NotPropertiesError if the current package properties are
    malformed."""
    package_properties = PackageProperties(name="invalid name with spaces").asdict
    path = write_json(package_properties, tmp_path / "datapackage.json")

    with raises(NotPropertiesError):
        edit_package_properties(path, properties)


def test_throws_error_if_new_package_properties_are_incorrect(properties_path):
    """Should throw NotPropertiesError if the new package properties are incorrect."""
    with raises(NotPropertiesError):
        edit_package_properties(properties_path, {})

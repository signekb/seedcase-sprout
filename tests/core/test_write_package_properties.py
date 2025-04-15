from dataclasses import replace
from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.core.properties import (
    LicenseProperties,
    PackageProperties,
    ResourceProperties,
)
from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.write_json import write_json
from seedcase_sprout.core.write_package_properties import write_package_properties

resource_properties = ResourceProperties(
    name="resource-1",
    path=str(Path("resources", "1", "data.parquet")),
    title="My First Resource",
    description="This is my first resource.",
)


@fixture
def package_properties() -> PackageProperties:
    return PackageProperties(
        name="my-package",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="2.0.0",
        created="2024-05-14T05:00:01+00:00",
        resources=[resource_properties],
        licenses=[LicenseProperties(name="license")],
    )


@fixture
def path(tmp_path) -> Path:
    return tmp_path / "datapackage.json"


def assert_file_contains(path: Path, expected_properties: PackageProperties):
    new_properties = read_json(path)
    assert new_properties == expected_properties.compact_dict


def test_writes_properties_when_file_does_not_exist(path, package_properties):
    """Should write properties to file when the file doesn't yet exist."""
    assert write_package_properties(package_properties, path) == path
    assert_file_contains(path, package_properties)


def test_rewrites_package_properties_when_file_exists(path, package_properties):
    """Should write properties to file when the file already exists, rewriting existing
    package properties."""
    old_properties = package_properties.compact_dict | {"name": "old-name"}
    write_json(old_properties, path)

    assert write_package_properties(package_properties, path) == path
    assert_file_contains(path, package_properties)


def test_rewrites_resource_properties_when_file_exists(path, package_properties):
    """Should write properties to file when the file already exists, rewriting existing
    resource properties."""
    old_properties = replace(
        package_properties,
        resources=[replace(resource_properties, name="old-name")],
    )
    write_json(old_properties.compact_dict, path)

    assert write_package_properties(package_properties, path) == path
    assert_file_contains(path, package_properties)


def test_writes_properties_with_missing_resources(path, package_properties):
    """Should write properties with missing resources to file."""
    write_json(package_properties.compact_dict, path)
    new_properties = replace(package_properties, resources=None)

    assert write_package_properties(new_properties, path) == path
    assert_file_contains(path, new_properties)


def test_throws_error_if_error_in_package_properties(path, package_properties):
    """Should throw `CheckError`s if there are errors in the package properties."""
    package_properties.name = "invalid name with spaces"
    package_properties.id = None
    write_json(resource_properties.compact_dict, path)

    with raises(ExceptionGroup):
        write_package_properties(package_properties, path)

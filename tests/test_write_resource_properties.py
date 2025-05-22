from json import JSONDecodeError
from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.examples import (
    ExamplePackage,
    example_package_properties,
)
from seedcase_sprout.internals import _read_json, _write_json
from seedcase_sprout.paths import PackagePath
from seedcase_sprout.properties import (
    LicenseProperties,
    PackageProperties,
    ResourceProperties,
)
from seedcase_sprout.write_package_properties import write_package_properties
from seedcase_sprout.write_resource_properties import write_resource_properties
from tests.assert_raises_errors import assert_raises_check_errors


@fixture
def resource_properties_1() -> ResourceProperties:
    return ResourceProperties(
        name="resource-1",
        title="My First Resource",
        description="This is my first resource.",
    )


@fixture
def resource_properties_2() -> ResourceProperties:
    return ResourceProperties(
        name="resource-2",
        title="My Second Resource",
        description="This is my second resource.",
    )


@fixture
def package_properties_path(
    tmp_path, resource_properties_1, resource_properties_2
) -> Path:
    package_properties = PackageProperties(
        name="my-package",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="2.0.0",
        created="2024-05-14T05:00:01+00:00",
        resources=[
            resource_properties_1.compact_dict,
            resource_properties_2.compact_dict,
        ],
        licenses=[LicenseProperties(name="license")],
    )
    return _write_json(package_properties.compact_dict, tmp_path / "datapackage.json")


def test_updates_existing_resource_in_package(
    package_properties_path, resource_properties_2
):
    """Given a package with a matching resource, should update the properties of
    this resource."""
    # given
    new_resource_properties = ResourceProperties(
        name="resource-1",
        title="My New Title",
        description="This is my updated resource.",
    )
    expected_resources = [
        new_resource_properties.compact_dict,
        resource_properties_2.compact_dict,
    ]

    # when
    path = write_resource_properties(new_resource_properties, package_properties_path)

    # then
    assert len(list(path.parent.iterdir())) == 1
    assert _read_json(path)["resources"] == expected_resources


def test_adds_new_resource_to_package(
    package_properties_path, resource_properties_1, resource_properties_2
):
    """Given a package without a matching resource, should add a new set of
    resource properties."""
    # given
    resource_properties_3 = ResourceProperties(
        name="resource-3",
        title="My Third Resource",
        description="This is my third resource.",
    )
    expected_resources = [
        resource_properties_1.compact_dict,
        resource_properties_2.compact_dict,
        resource_properties_3.compact_dict,
    ]

    # when
    path = write_resource_properties(resource_properties_3, package_properties_path)

    # then
    assert path == package_properties_path
    assert len(list(path.parent.iterdir())) == 1
    assert _read_json(path)["resources"] == expected_resources


def test_error_if_path_points_to_dir(tmp_path):
    """Should have an error if the path points to a folder."""
    with raises(FileNotFoundError):
        write_resource_properties(ResourceProperties(), tmp_path)


def test_error_if_path_points_to_nonexistent_file(tmp_path):
    """Should have an error if the path points to a nonexistent file."""
    with raises(FileNotFoundError):
        write_resource_properties(ResourceProperties(), tmp_path / "datapackage.json")


def test_error_if_properties_file_cannot_be_read(tmp_path, resource_properties_1):
    """Should have an error if the properties file cannot be read as JSON."""
    file_path = tmp_path / "datapackage.json"
    file_path.write_text(",,, this is not, JSON")

    with raises(JSONDecodeError):
        write_resource_properties(resource_properties_1, file_path)


def test_error_if_input_resource_properties_are_incorrect(
    package_properties_path,
):
    """Should raise an error if the input resource properties are incorrect."""
    assert_raises_check_errors(
        lambda: write_resource_properties(ResourceProperties(), package_properties_path)
    )


def test_error_if_existing_resource_properties_are_incorrect(
    resource_properties_1, resource_properties_2
):
    """Should raise an error if the existing resource properties are incorrect."""
    delattr(resource_properties_1, "name")
    package_properties = example_package_properties()
    package_properties.resources = [resource_properties_1]
    with ExamplePackage() as package_path:
        _write_json(package_properties.compact_dict, package_path.properties())

        assert_raises_check_errors(
            lambda: write_resource_properties(resource_properties_2)
        )


def test_error_if_package_properties_have_missing_required_fields(
    tmp_path, resource_properties_1
):
    """Should have an error if there are missing properties in the file."""
    path = _write_json({}, tmp_path / "datapackage.json")

    with raises(ExceptionGroup):
        write_resource_properties(resource_properties_1, path)


def test_writes_properties_to_cwd_if_no_path_provided(tmp_cwd, resource_properties_1):
    """If no path is provided, should use datapackage.json in the cwd."""
    properties_path = PackagePath(tmp_cwd).properties()
    write_package_properties(example_package_properties(), properties_path)

    assert write_resource_properties(resource_properties_1) == properties_path


def test_fails_correctly_if_no_path_provided_and_no_properties_in_cwd(
    tmp_cwd, resource_properties_1
):
    """Should throw the expected error if no path is provided and there is no
    datapackage.json in the cwd."""
    with raises(FileNotFoundError):
        write_resource_properties(resource_properties_1)

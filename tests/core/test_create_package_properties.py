from pytest import fixture, raises

from seedcase_sprout.core import (
    ContributorProperties,
    LicenseProperties,
    PackageProperties,
)
from seedcase_sprout.core.create_package_properties import create_package_properties
from seedcase_sprout.core.read_json import read_json


@fixture
def package_properties() -> PackageProperties:
    return PackageProperties(
        name="test-package",
        title="Test of data package",
        description="Data for a test data package.",
        contributors=[
            ContributorProperties(
                title="Luke",
                email="luke@example.com",
                roles=["creator"],
            )
        ],
        licenses=[
            LicenseProperties(
                name="ODC-BY-1.0",
                path="https://opendatacommons.org/licenses/by",
                title="Open Data Commons Attribution License 1.0",
            )
        ],
    )


def test_creates_folder_and_file_correctly(package_properties, tmp_path):
    """Given a path, should create the correct folder and file."""
    # given
    expected_package_path = tmp_path
    expected_properties_path = expected_package_path / "datapackage.json"

    # when
    path = create_package_properties(package_properties, tmp_path)

    # then
    assert len(list(tmp_path.iterdir())) == 1
    assert expected_package_path.is_dir()
    assert len(list(expected_package_path.iterdir())) == 1
    assert path == expected_properties_path
    assert expected_properties_path.is_file()


def test_writes_nonempty_files(package_properties, tmp_path):
    """The files written should not be empty. The properties file should be parsable as
    JSON."""
    properties_path = create_package_properties(package_properties, tmp_path)

    assert read_json(properties_path)


def test_throws_error_if_path_points_to_file(package_properties, tmp_path):
    """Raises NotADirectoryError if the input path points to a file."""
    file_path = tmp_path / "datapackage.json"
    file_path.touch()

    with raises(NotADirectoryError):
        create_package_properties(package_properties, file_path)


def test_explicitly_set_values_not_overwritten_by_defaults(
    package_properties, tmp_path
):
    """When the properties have non-empty values set for the listed fields, these are
    not overwritten by default values."""
    this_uuid = "123e4567-e89b-12d3-a456-426614174000"
    random_timestamp = "2021-09-01T12:00:00Z"
    package_properties.id = this_uuid
    package_properties.version = "0.2.0"
    package_properties.created = random_timestamp

    properties_path = create_package_properties(package_properties, tmp_path)
    properties = read_json(properties_path)

    assert properties["version"] == "0.2.0"
    assert properties["created"] == random_timestamp
    assert properties["id"] == this_uuid

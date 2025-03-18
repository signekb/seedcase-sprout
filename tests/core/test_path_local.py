from pathlib import Path

from pytest import fixture, mark, raises

from seedcase_sprout.core import (
    path_properties,
    path_readme,
    path_resource,
    path_resource_batch,
    path_resource_batch_files,
    path_resource_data,
    path_resources,
)
from tests.core.directory_structure_setup import (
    create_test_data_package,
    create_test_resource_structure,
)


@fixture
def tmp_package(tmp_path):
    """Set up a test data package with two resources."""
    create_test_data_package(tmp_path)

    create_test_resource_structure(tmp_path, ["batch_file_1.csv.gz"])
    create_test_resource_structure(
        tmp_path, ["batch_file_2.csv.gz", "batch_file_3.csv.gz"]
    )

    return tmp_path


@mark.parametrize(
    "function, expected_path",
    [
        (path_properties, "datapackage.json"),
        (path_readme, "README.md"),
    ],
)
def test_path_local_root_functions_return_expected_path(
    tmp_path, tmp_package, function, expected_path
):
    path = function(path=tmp_path)
    assert path == tmp_package / expected_path
    assert path.is_file()


@mark.parametrize(
    "function, expected_path",
    [
        (path_resource, "resources/2"),
        (path_resource_data, "resources/2/data.parquet"),
        (path_resource_batch, "resources/2/batch"),
    ],
)
def test_path_resource_functions_return_expected_path(
    tmp_path, tmp_package, function, expected_path
):
    """Test that the path to the resource is returned correctly and exists."""
    path = function(resource_id=2, path=tmp_path)
    # When, then
    assert path == tmp_package / expected_path
    assert path.is_file() or path.is_dir()


@mark.parametrize(
    "function",
    [path_properties, path_readme],
)
def test_path_local_root_functions_raise_error_if_files_not_exist(
    tmp_package, function
):
    """Test that an error is raised if the file does not exist"""
    # Given
    function(path=tmp_package).unlink()
    # When, then
    with raises(FileNotFoundError):
        function(path=tmp_package)


def test_path_resources_returns_expected_path(tmp_path, tmp_package):
    """Test that the path to the resources directory is returned correctly"""
    # When, then
    assert path_resources(path=tmp_path) == tmp_package / "resources"


def test_path_resource_batch_files_returns_expected_list_of_paths(tmp_package):
    """Test that batch files are listed correctly"""
    # When
    resource_batch_path = Path(tmp_package) / "resources" / "2" / "batch"
    # Then
    assert set(path_resource_batch_files(resource_id=2, path=tmp_package)) == set(
        [
            resource_batch_path / "batch_file_2.csv.gz",
            resource_batch_path / "batch_file_3.csv.gz",
        ]
    )


@mark.parametrize(
    "function",
    [
        path_resource,
        path_resource_data,
        path_resource_batch,
        path_resource_batch_files,
    ],
)
def test_path_resource_functions_raise_error_if_res_id_does_not_exist(
    tmp_package, function
):
    """Raises error if resource ID doesn't exist"""
    # When, then
    with raises(NotADirectoryError):
        function(resource_id=3, path=tmp_package)

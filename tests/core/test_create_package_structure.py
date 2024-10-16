from pytest import raises

from sprout.core.create_package_structure import create_package_structure
from sprout.core.read_json import read_json


def test_creates_folder_structure_correctly(tmp_path):
    """Given a path, should create the correct folders and files."""
    # given
    expected_package_path = tmp_path / "1"
    expected_properties_path = expected_package_path / "datapackage.json"
    expected_readme_path = expected_package_path / "README.md"
    expected_resources_dir = expected_package_path / "resources"

    # when
    paths = create_package_structure(tmp_path)

    # then
    assert len(list(tmp_path.iterdir())) == 1
    assert expected_package_path.is_dir()
    assert len(list(expected_package_path.iterdir())) == 3
    assert paths == [
        expected_properties_path,
        expected_readme_path,
        expected_resources_dir,
    ]
    assert expected_properties_path.is_file()
    assert expected_readme_path.is_file()


def test_writes_nonempty_files(tmp_path):
    """The files written should not be empty. The properties file should be parsable as
    JSON."""
    properties_path, readme_path, resource_dir = create_package_structure(tmp_path)

    assert read_json(properties_path)
    assert readme_path.read_text()
    assert resource_dir.is_dir()


def test_throws_error_if_directory_does_not_exist(tmp_path):
    """Raises NotADirectoryError if the input path points to a nonexistent folder."""
    with raises(NotADirectoryError):
        create_package_structure(tmp_path / "nonexistent")


def test_throws_error_if_path_points_to_file(tmp_path):
    """Raises NotADirectoryError if the input path points to a file."""
    file_path = tmp_path / "test.txt"
    file_path.touch()

    with raises(NotADirectoryError):
        create_package_structure(file_path)

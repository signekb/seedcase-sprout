from pytest import raises

import sprout.core as sp


def test_returns_resource_structure_when_no_resources_exist(tmp_path):
    """Returns the paths to the resource and raw data folder."""
    lst_created_paths = sp.create_resource_structure(tmp_path)

    assert lst_created_paths[0].is_dir()
    assert lst_created_paths[1].is_dir()
    assert lst_created_paths == [tmp_path / "1", tmp_path / "1" / "raw"]


def test_returns_resource_structure_when_resources_exist(tmp_path):
    """Returns the paths to the resource and raw data folder with the next id."""
    # Create first resource structure
    sp.create_resource_structure(tmp_path)

    # Create new resource structure
    lst_created_paths = sp.create_resource_structure(tmp_path)

    assert lst_created_paths[0].is_dir()
    assert lst_created_paths[1].is_dir()
    assert lst_created_paths == [tmp_path / "2", tmp_path / "2" / "raw"]


def test_raises_not_a_directory_error(tmp_path):
    """Raises NotADirectoryError when the path is not an existing directory."""
    with raises(NotADirectoryError):
        sp.create_resource_structure(tmp_path / "non_existent_folder")

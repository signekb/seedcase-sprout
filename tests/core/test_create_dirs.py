from pytest import raises

from seedcase_sprout.core.create_dirs import create_dirs


def test_create_single_dir(tmp_path):
    """Create a new directory and return the path correctly."""
    # Create a temporary directory
    new_dir = [tmp_path / "new_dir"]

    result = create_dirs(new_dir)

    # Check if the dir is created
    assert new_dir[0].exists()

    # Check if the result is equal to the new directory
    assert result[0] == new_dir[0]


def test_create_two_dirs(tmp_path):
    """Create a number of new directories and returns the paths correctly."""
    # Create a temporary directory
    new_dirs = [
        tmp_path / "new_dir1",
        tmp_path / "new_dir2",
    ]

    result = create_dirs(new_dirs)

    # Check if the dirs are created
    assert new_dirs[0].exists()
    assert new_dirs[1].exists()

    # Check if the result is equal to the new directory
    assert result == new_dirs


def test_raise_error_with_existing_dir(tmp_path):
    """Raise FileExistsError when the input path is an existent directory."""
    # Create a temporary directory
    new_dir = [tmp_path / "new_dir"]
    new_dir[0].mkdir()

    with raises(
        FileExistsError,
    ):
        create_dirs(new_dir)

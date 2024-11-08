from pytest import raises

from seedcase_sprout.core.verify_is_dir import verify_is_dir


def test_returns_existing_directory(tmp_path):
    """Test the path is returned if the directory exists."""
    assert verify_is_dir(tmp_path) == tmp_path


def test_raises_error_with_non_existent_directory(tmp_path):
    """Test that NotADirectoryError is raised if the directory doesn't exist."""
    with raises(
        NotADirectoryError,
        match=r"/non_existent_directory",
    ):
        verify_is_dir(tmp_path / "non_existent_directory")


def test_returns_error_with_file(tmp_path):
    """Test that NotADirectoryError is raised when a file path is given as input."""

    file_path = tmp_path / "test.py"
    file_path.write_text("# This is a temporary Python file")

    assert file_path.is_file()

    with raises(
        NotADirectoryError,
        match=r"/test.py",
    ):
        verify_is_dir(file_path)

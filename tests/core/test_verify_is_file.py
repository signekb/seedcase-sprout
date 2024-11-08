from pytest import raises

from seedcase_sprout.core.verify_is_file import verify_is_file


def test_returns_file_with_valid_path(tmp_path):
    """Test that a file is returned when given a valid path."""
    file_path = tmp_path / "existing_file.txt"
    file_path.touch()  # Create a file at the path
    assert verify_is_file(file_path) == file_path


def test_raises_error_with_non_existent_file(tmp_path):
    """Test that FileNotFoundError is raised if the file doesn't exist."""
    with raises(FileNotFoundError):
        verify_is_file(tmp_path / "non_existent_file.txt")

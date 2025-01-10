from pathlib import Path


def check_is_dir(path: Path) -> Path:
    """Checks whether the path exists and is a directory.

    Args:
        path: The path to check.

    Returns:
        The path if it is a directory.

    Raises:
        NotADirectoryError: If path either doesn't exist or isn't a directory.
    """
    if not path.is_dir():
        raise NotADirectoryError(f"{path} either doesn't exist or isn't a directory.")

    return path

from pathlib import Path


def verify_is_dir(path: Path) -> Path:
    """Verifies whether the directory given by the path exists or not.

    Args:
        path: The path to verify

    Raises:
        NotADirectoryError: When the directory in the path doesn't exist.

    Returns:
        A Path object if it is a directory.
    """
    if not path.is_dir():
        raise NotADirectoryError(f"{path} either isn't a directory or doesn't exist.")

    return path

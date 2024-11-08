from pathlib import Path


def verify_is_file(path: Path) -> Path:
    """Verifies whether the file given by the path exists or not.

    Args:
        path: The path to verify.

    Raises:
        FileNotFound: When the file in the path doesn't exist.

    Returns:
        A Path object if it is a file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"{path} is not a file.")

    return path

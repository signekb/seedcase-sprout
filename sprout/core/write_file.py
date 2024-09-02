from pathlib import Path


def write_file(string: str, path: Path) -> Path:
    """Writes a file to the given path with the given content.

    The parent folder of the file given in path must exist.
    If the file already exists, it will be overwritten.

    Args:
        string: Content to be written to the file.
        path: Path of the file to be created, including file name and extension.

    Returns:
        A path to the file that was created.

    Raises:
        FileNotFoundError: If the parent folder of the file doesn't exist.
    """
    path.write_text(string)

    return path

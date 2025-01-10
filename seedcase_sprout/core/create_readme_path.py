from pathlib import Path


def create_readme_path(path: Path) -> Path:
    """Creates the path to the README of the specified package.

    Args:
        path: The path to the package folder.

    Returns:
        The path to the package's README.
    """
    return path / "README.md"

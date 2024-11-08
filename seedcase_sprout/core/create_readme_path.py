from pathlib import Path


def create_readme_path(path: Path) -> Path:
    """Returns the path to the README of the specified package.

    Args:
        path: the path to the package folder

    Returns:
        the path to the package README
    """
    return path / "README.md"

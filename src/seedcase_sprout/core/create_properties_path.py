from pathlib import Path


def create_properties_path(path: Path) -> Path:
    """Creates the path to the package's properties file.

    Args:
        path: The path to the package folder.

    Returns:
        The path to the properties file.
    """
    return path / "datapackage.json"

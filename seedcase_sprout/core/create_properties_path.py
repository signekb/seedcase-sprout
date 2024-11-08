from pathlib import Path


def create_properties_path(path: Path) -> Path:
    """Returns the path to the datapackage.json file of the package.

    Args:
        path: the path to the package folder

    Returns:
        the path to datapackage.json
    """
    return path / "datapackage.json"

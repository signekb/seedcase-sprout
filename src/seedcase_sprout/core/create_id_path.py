from pathlib import Path


def create_id_path(path: Path, id: int) -> Path:
    """Create a path for a new package or resource.

    Args:
        path: The path to the package folder or the resources folder within the package
        id: The ID of the package or resource

    Returns:
        The path to the package or resource
    """
    return path / f"{id}"

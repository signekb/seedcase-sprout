from pathlib import Path


def create_resource_raw_path(path: Path) -> Path:
    """Creates a path to the raw directory for a resource.

    Args:
        path: The directory to create the new raw directory in.

    Returns:
        The path to the resource's raw folder.
    """
    return path / "raw"

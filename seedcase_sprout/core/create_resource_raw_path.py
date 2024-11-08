from pathlib import Path


def create_resource_raw_path(path: Path) -> Path:
    """Create a path to the raw directory for a resource.

    Args:
        path: Directory to create the new raw directory in.

    Returns:
        A path to the folder.
    """
    return path / "raw"

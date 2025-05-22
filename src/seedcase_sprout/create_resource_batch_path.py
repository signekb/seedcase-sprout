from pathlib import Path


def create_resource_batch_path(path: Path) -> Path:
    """Creates a path to the batch directory for a resource.

    Args:
        path: The directory to create the new batch directory in.

    Returns:
        The path to the resource's batch folder.
    """
    return path / "batch"

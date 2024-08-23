from pathlib import Path


def create_relative_resource_data_path(path: Path) -> Path:
    """Create a relative path to the resource data file.

    Args:
        path: Absolute path to the folder of a specific resource

    Returns:
        Relative path from the package root to the resource data file
        E.g., "resources/1/data.parquet"
    """
    return Path(*path.parts[-2:]) / "data.parquet"

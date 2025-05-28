from pathlib import Path


def _create_resource_data_path(resource_name: str) -> str:
    """Creates a stringified relative path to the resource data file based on the name.

    Args:
        resource_name: The name of the resource.

    Returns:
        The relative path from the package root to the resource data file.
            E.g., "resources/test-resource/data.parquet"
    """
    return str(Path("resources", resource_name, "data.parquet"))

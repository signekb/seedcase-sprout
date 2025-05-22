from pathlib import Path
from typing import Any

from seedcase_sprout.sprout_checks.is_resource_name_correct import (
    _is_resource_name_correct,
)


def _create_relative_resource_data_path(resource_name: Any) -> str | None:
    """Creates a stringified relative path to the resource data file based on the name.

    The path is created only if the resource name is correct.

    Args:
        resource_name: The name of the resource.

    Returns:
        The relative path from the package root to the resource data file.
            E.g., "resources/test-resource/data.parquet"
    """
    return (
        str(Path("resources", resource_name, "data.parquet"))
        if _is_resource_name_correct(resource_name)
        else None
    )

from pathlib import Path

from seedcase_sprout.core.checks.check_error import CheckError
from seedcase_sprout.core.sprout_checks.get_json_path_to_resource_field import (
    get_json_path_to_resource_field,
)


def check_id_in_resource_path(
    properties: dict, index: int | None = None
) -> list[CheckError]:
    """Checks if the data path in resource properties is well-formed.

    Ignores a missing data path or a path of the wrong type.

    Args:
        properties: The resource properties to check.
        index: The index of the resource properties. Defaults to None.

    Returns:
        The properties, if the data path is well-formed.
    """
    data_path = properties.get("path")
    if not isinstance(data_path, str):
        return []

    data_path = Path(data_path)
    if len(data_path.parts) == 3 and data_path.parts[1].isdigit():
        return []

    return [
        CheckError(
            message="'path' should contain the resource ID",
            json_path=get_json_path_to_resource_field("path", index),
            validator="pattern",
        )
    ]

from pathlib import Path

from frictionless.errors import ResourceError

from seedcase_sprout.core.not_properties_error import NotPropertiesError


def check_data_path(properties: dict) -> dict:
    """Checks if the data path in the resource properties is well-formed.

    Args:
        properties: The resource properties to check.

    Returns:
        The properties, if the data path is well formed.

    Raises:
        NotPropertiesError: If the data path is not well formed.
    """
    data_path = Path(properties.get("path", ""))
    if len(data_path.parts) != 3 or not data_path.parts[1].isdigit():
        error = ResourceError(
            note=(
                "No resource ID found in the field `path` in resource properties. The "
                "`path` field on the resource should point to the associated data "
                "file. Are you sure you set up the resource correctly?"
            )
        )
        raise NotPropertiesError([error], properties)

    return properties

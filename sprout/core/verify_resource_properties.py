from pathlib import Path

from frictionless.errors import ResourceError

from sprout.core.not_properties_error import NotPropertiesError
from sprout.core.verify_properties_are_complete import verify_properties_are_complete
from sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)

REQUIRED_RESOURCE_PROPERTIES = {"name", "path", "title", "description"}


def verify_resource_properties(properties: dict) -> dict:
    """Verifies if a set of resource properties is correct.

    The resource properties are correct if they conform to the Data Resource
    specification and they contain non-empty values for all required resource
    properties fields. They should also have a well-formed value for `path`.

    Args:
        properties: The resource properties to verify.

    Returns:
        The resource properties, if correct.

    Raises:
        NotPropertiesError: If the resource properties are not correct.
    """
    verify_properties_are_complete(
        properties, ResourceError, REQUIRED_RESOURCE_PROPERTIES
    )
    verify_properties_are_well_formed(properties, ResourceError.type)
    verify_data_path(properties)

    return properties


def verify_data_path(properties: dict) -> dict:
    """Checks if the data path on the resource properties is well formed.

    Args:
        properties: The resource properties to check.

    Returns:
        The properties, if the data path is well formed.

    Raises:
        NotPropertiesError: If the data path is not well formed.
    """
    data_path = Path(properties["path"])
    if len(data_path.parts) != 3 or not data_path.parts[1].isdigit():
        error = ResourceError(
            note=(
                "No resource ID found on resource properties. The `path` field on the "
                "resource should point to the associated data file. "
                "Are you sure you set up the resource correctly?"
            )
        )
        raise NotPropertiesError([error], properties)

    return properties

from frictionless.errors import ResourceError

from sprout.core.verify_data_path import verify_data_path
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

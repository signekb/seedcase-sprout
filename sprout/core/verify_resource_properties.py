from frictionless import Resource

from sprout.core.not_properties_error import NotPropertiesError


def verify_resource_properties(properties: dict) -> dict:
    """Checks if the resource properties provided are valid.

    Args:
        properties: the resource properties to check

    Raises:
        NotPropertiesError: if Frictionless finds an error in the properties

    Returns:
        the properties, if valid
    """
    report = Resource.validate_descriptor(properties)
    if not report.valid:
        raise NotPropertiesError(report.errors, properties)
    return properties

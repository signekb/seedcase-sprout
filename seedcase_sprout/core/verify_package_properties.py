from frictionless.errors import PackageError

from seedcase_sprout.core.verify_properties_are_complete import (
    verify_properties_are_complete,
)
from seedcase_sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)

REQUIRED_PACKAGE_PROPERTIES = {
    "name",
    "id",
    "title",
    "description",
    "version",
    "created",
    "resources",
}


def verify_package_properties(properties: dict) -> dict:
    """Verifies if a set of package properties is correct.

    The package properties are correct if they conform to the Data Package
    specification and they contain non-empty values for all required package
    properties fields.

    Args:
        properties: The package properties to verify.

    Returns:
        The package properties, if correct.

    Raises:
        NotPropertiesError: If the package properties are not correct.
    """
    verify_properties_are_complete(
        properties, PackageError, REQUIRED_PACKAGE_PROPERTIES
    )
    verify_properties_are_well_formed(properties, PackageError.type)

    return properties

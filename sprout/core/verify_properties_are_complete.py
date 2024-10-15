from typing import Type

from frictionless.errors import PackageError, ResourceError

from sprout.core.not_properties_error import NotPropertiesError


def verify_properties_are_complete(
    properties: dict,
    error_class: Type[PackageError | ResourceError],
    required_fields: set[str],
) -> dict:
    """Verifies that all required fields are present on `properties` and not empty.

    Args:
        properties: The properties to verify.
        error_class: The Frictionless class corresponding to the type of error to raise.
        required_fields: A set containing the names of the required fields.

    Returns:
        The properties, if complete.

    Raises:
        NotPropertiesError: If the properties are not complete.
    """
    errors = [
        error_class(note=f"'{field}' is a required property and cannot be empty.")
        for field in required_fields
        # N.B. that an empty list is an acceptable value for a required field.
        if properties.get(field) in ["", None]
    ]

    if errors:
        raise NotPropertiesError(errors, properties)

    return properties

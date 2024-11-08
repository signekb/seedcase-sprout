from frictionless import validate
from frictionless.errors import Error

from seedcase_sprout.core.not_properties_error import NotPropertiesError


def verify_properties_are_well_formed(properties: dict, error_type: str) -> dict:
    """Verifies if the properties provided have the correct structure.

    This function checks that `properties` contains the fields expected by the Data
    Package spec. At this point, empty values are not checked against format
    constraints. This function takes into account only errors specific to the type of
    metadata being verified.

    Args:
        properties: The properties to verify.
        error_type: The type of Frictionless error to filter for.

    Returns:
        The properties, if well-formed.

    Raises:
        NotPropertiesError: If the properties are not well-formed.
    """
    non_empty_properties = {
        key: value for key, value in properties.items() if value != ""
    }
    report = validate(non_empty_properties, type=error_type.replace("-error", ""))

    errors = [
        error
        for error in report.errors
        if "required" not in error.message and error.type == error_type
    ]

    if properties == {}:
        errors = [Error(note="Empty properties provided")]

    if errors:
        raise NotPropertiesError(errors, properties)

    return properties

from frictionless import validate

from sprout.core.not_properties_error import NotPropertiesError


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
    report = validate(non_empty_properties)

    errors = [
        error
        for error in report.errors
        + [error for task in report.tasks for error in task.errors]
        if error.type == error_type
    ]
    if errors:
        raise NotPropertiesError(errors, properties)

    return properties

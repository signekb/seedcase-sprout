from frictionless import Report, Resource


class InvalidResourcePropertiesError(Exception):
    """Raised if the resource properties are invalid."""

    def __init__(self, report: Report, properties: dict, *args, **kwargs):
        """Initialises InvalidResourcePropertiesError.

        Args:
            report: validation report provided by Frictionless
            properties: invalid resource properties
            *args: non-keyword arguments
            **kwargs: keyword arguments
        """
        # TODO: Consider if it's a problem for us that report.errors is not guaranteed
        # to include all errors.
        errors = [
            f"{error.title}: {error.description} {error.message}"
            for error in report.errors
        ]
        message = (
            f"Invalid resource properties provided:\n{properties}"
            f"\nThe following errors were found:\n{'\n'.join(errors)}"
        )
        super().__init__(message, *args, **kwargs)


def verify_resource_properties(properties: dict) -> dict:
    """Checks if the resource properties provided are valid.

    Args:
        properties: the resource properties to check

    Raises:
        InvalidResourcePropertiesError: if Frictionless finds an error in the properties

    Returns:
        the properties, if valid
    """
    report = Resource.validate_descriptor(properties)
    if not report.valid:
        raise InvalidResourcePropertiesError(report, properties)
    return properties

from frictionless import Error


class NotPropertiesError(Exception):
    """Raised for incorrect properties objects."""

    def __init__(self, errors: list[Error], properties: dict, *args, **kwargs):
        """Initialises NotPropertiesError.

        Args:
            errors: List of Frictionless errors.
            properties: Incorrect properties.
            *args: Non-keyword arguments.
            **kwargs: Keyword arguments.
        """
        # TODO: Consider if it's a problem for us that errors from frictionless reports
        # are not guaranteed to include all errors.
        errors = [
            f"{error.title}: {error.description} {error.message}" for error in errors
        ]
        message = (
            f"Incorrect properties provided:\n{properties}"
            f"\nThe following errors were found:\n{'\n'.join(errors)}"
        )
        super().__init__(message, *args, **kwargs)

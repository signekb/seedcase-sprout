from jsonschema import ValidationError


def unwrap_errors(errors: list[ValidationError]) -> list[ValidationError]:
    """Recursively extracts all errors into a flat list of errors.

    Args:
        errors: A nested list of errors.

    Returns:
        A flat list of errors.
    """
    unwrapped = []
    for error in errors:
        unwrapped.append(error)
        if error.context:
            unwrapped.extend(unwrap_errors(error.context))
    return unwrapped

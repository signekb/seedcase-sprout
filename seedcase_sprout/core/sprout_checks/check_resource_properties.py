from seedcase_sprout.core import checks
from seedcase_sprout.core.sprout_checks.exclude_non_sprout_resource_errors import (
    exclude_non_sprout_resource_errors,
)
from seedcase_sprout.core.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)


def check_resource_properties(properties: dict, check_required: bool = True) -> dict:
    """Checks that resource `properties` matches requirements in Sprout.

    `properties` is checked against the Data Package standard and the following
    Sprout-specific requirements:
      - Sprout-specific required fields are present
      - Required fields are not blank
      - `path` is of type string
      - `path` includes resource ID
      - `data` is not set

    Only resource properties are checked.

    Args:
        properties: The resource properties to check.
        check_required: Whether the function should enforce the presence of required
            fields. Defaults to True.

    Returns:
        `properties`, if all checks passed.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    errors = checks.check_resource_properties(properties)
    errors = exclude_non_sprout_resource_errors(errors)

    if not check_required:
        errors = [error for error in errors if error.validator != "required"]

    errors += get_sprout_resource_errors(properties, check_required)
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed for the resource properties:\n{properties}",
            errors,
        )

    return properties

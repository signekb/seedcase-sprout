from seedcase_sprout.core import checks
from seedcase_sprout.core.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)


def check_package_properties(properties: dict, check_required=True) -> dict:
    """Checks that package `properties` matches requirements in Sprout.

    `properties` is checked against the Data Package standard and the following
    Sprout-specific requirements:
      - Sprout-specific required fields are present
      - Required fields are not blank

    Only package properties are checked.

    Args:
        properties: The package properties to check.
        check_required: Whether the function should enforce the presence of required
            fields. Defaults to True.

    Returns:
        `properties` if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one for each check that failed.
    """
    errors = checks.check_package_properties(properties)

    if not check_required:
        errors = [error for error in errors if error.validator != "required"]

    errors += get_sprout_package_errors(properties, check_required)
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed on the package properties:\n{properties}",
            errors,
        )

    return properties

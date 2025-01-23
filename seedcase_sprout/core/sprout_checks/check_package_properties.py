from seedcase_sprout.core import checks
from seedcase_sprout.core.checks.check_error_matcher import CheckErrorMatcher
from seedcase_sprout.core.checks.exclude_matching_errors import exclude_matching_errors
from seedcase_sprout.core.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)


def check_package_properties(
    properties: dict, ignore: list[CheckErrorMatcher] = []
) -> dict:
    """Checks that package `properties` matches requirements in Sprout.

    `properties` is checked against the Data Package standard and the following
    Sprout-specific requirements:
      - Sprout-specific required fields are present
      - Required fields are not blank

    Only package properties are checked.

    Args:
        properties: The package properties to check.
        ignore: A list of matchers for any `CheckErrors` to ignore.

    Returns:
        `properties` if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    errors = checks.check_package_properties(properties) + get_sprout_package_errors(
        properties
    )
    errors = exclude_matching_errors(errors, ignore)
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed on the package properties:\n{properties}",
            errors,
        )

    return properties

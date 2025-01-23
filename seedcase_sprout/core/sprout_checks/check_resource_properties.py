from seedcase_sprout.core import checks
from seedcase_sprout.core.checks.check_error_matcher import CheckErrorMatcher
from seedcase_sprout.core.checks.exclude_matching_errors import exclude_matching_errors
from seedcase_sprout.core.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)


def check_resource_properties(
    properties: dict, ignore: list[CheckErrorMatcher] = []
) -> dict:
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
        ignore: A list of matchers for any `CheckErrors` to ignore.

    Returns:
        `properties`, if all checks passed.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    errors = checks.check_resource_properties(properties) + get_sprout_resource_errors(
        properties
    )
    errors = exclude_matching_errors(
        errors,
        [
            *ignore,
            CheckErrorMatcher(validator="required", json_path="data"),
            CheckErrorMatcher(
                validator="type", json_path="path", message="not of type 'array'"
            ),
        ],
    )
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed for the resource properties:\n{properties}",
            errors,
        )

    return properties

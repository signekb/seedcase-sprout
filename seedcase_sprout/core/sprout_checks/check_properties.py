from seedcase_sprout.core import checks
from seedcase_sprout.core.checks.check_error_matcher import CheckErrorMatcher
from seedcase_sprout.core.checks.exclude_matching_errors import exclude_matching_errors
from seedcase_sprout.core.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)
from seedcase_sprout.core.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)

RESOURCE_FIELD_PATTERN = r"resources\[\d+\]"


def check_properties(properties: dict, ignore: list[CheckErrorMatcher] = []) -> dict:
    """Checks that `properties` matches requirements in Sprout.

    `properties` is checked against the Data Package standard and the following
    Sprout-specific requirements:
      - Sprout-specific required fields are present
      - Required fields are not blank
      - Resource `path` is of type string
      - Resource `path` includes resource ID
      - Resource `data` is not set

    Both package and resource properties are checked.

    Args:
        properties: The full package properties to check, including resource properties.
        ignore: A list of matchers for any `CheckErrors` to ignore.

    Returns:
        `properties`, if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    errors = checks.check_properties(properties)
    errors += get_sprout_package_errors(properties)

    if isinstance(properties.get("resources"), list):
        for index, resource in enumerate(properties.get("resources")):
            errors += get_sprout_resource_errors(resource, index)

    errors = exclude_matching_errors(
        errors,
        [
            *ignore,
            CheckErrorMatcher(
                validator="required", json_path=rf"{RESOURCE_FIELD_PATTERN}\.data$"
            ),
            CheckErrorMatcher(
                validator="type",
                json_path=rf"{RESOURCE_FIELD_PATTERN}\.path$",
                message="not of type 'array'",
            ),
        ],
    )
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed on the properties:\n{properties}", errors
        )

    return properties

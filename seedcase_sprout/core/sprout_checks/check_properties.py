from seedcase_sprout.core import checks
from seedcase_sprout.core.sprout_checks.exclude_non_sprout_resource_errors import (
    exclude_non_sprout_resource_errors,
)
from seedcase_sprout.core.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)
from seedcase_sprout.core.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)


def check_properties(properties: dict, check_required=True) -> dict:
    """Checks that `properties` matches requirements in Sprout.

    `properties` is checked against the Data Package standard and Sprout-specific
    requirements. Both package and resource properties are checked.

    Args:
        properties: The full package properties to check, including resource properties.
        check_required: Whether the function should enforce the presence of required
            fields. Defaults to True.

    Returns:
        `properties`, if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    errors = checks.check_properties(properties)
    errors = exclude_non_sprout_resource_errors(errors)

    if not check_required:
        errors = [error for error in errors if error.validator != "required"]

    errors += get_sprout_package_errors(properties, check_required)

    for index, resource in enumerate(properties.get("resources", [])):
        errors += get_sprout_resource_errors(resource, check_required, index)

    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The follow checks failed on the properties:\n{properties}", errors
        )

    return properties

import seedcase_sprout.core.checks as checks
from seedcase_sprout.core.sprout_checks.check_fields_not_blank import (
    check_fields_not_blank,
)
from seedcase_sprout.core.sprout_checks.check_fields_present import (
    check_fields_present,
)
from seedcase_sprout.core.sprout_checks.check_id_in_resource_path import (
    check_id_in_resource_path,
)
from seedcase_sprout.core.sprout_checks.check_no_inline_data import check_no_inline_data
from seedcase_sprout.core.sprout_checks.check_resource_path_string import (
    check_resource_path_string,
)
from seedcase_sprout.core.sprout_checks.required_fields import (
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)


def get_sprout_resource_errors(
    properties: dict, check_required: bool, index: int | None = None
) -> list[checks.CheckError]:
    """Checks the resource `properties` against Sprout-specific requirements only.

    Args:
        properties: The resource properties.
        check_required: Whether the function should enforce the presence of required
            fields.
        index: The index of the resource properties. Defaults to None.

    Returns:
        A list of errors. An empty list if no errors were found.
    """
    errors = check_resource_path_string(properties, index)
    errors += check_id_in_resource_path(properties, index)
    errors += check_no_inline_data(properties, index)
    errors += check_fields_not_blank(
        properties,
        RESOURCE_SPROUT_REQUIRED_FIELDS,
        index,
    )

    if check_required:
        errors += check_fields_present(
            properties, RESOURCE_SPROUT_REQUIRED_FIELDS, index
        )

    return errors

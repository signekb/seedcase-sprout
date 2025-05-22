from typing import Iterator

from jsonschema import ValidationError

from seedcase_sprout.check_datapackage.check_error import CheckError
from seedcase_sprout.check_datapackage.constants import COMPLEX_VALIDATORS
from seedcase_sprout.check_datapackage.get_full_json_path_from_error import (
    get_full_json_path_from_error,
)
from seedcase_sprout.check_datapackage.unwrap_errors import unwrap_errors


def validation_errors_to_check_errors(
    validation_errors: Iterator[ValidationError],
) -> list[CheckError]:
    """Transforms `jsonschema.ValidationError`s to more compact `CheckError`s.

    The list of errors is:

      - flattened
      - filtered for summary-type errors
      - filtered for duplicates
      - sorted by error location

    Args:
        validation_errors: The `jsonschema.ValidationError`s to transform.

    Returns:
        A list of `CheckError`s.
    """
    check_errors = [
        CheckError(
            message=error.message,
            json_path=get_full_json_path_from_error(error),
            validator=error.validator,
        )
        for error in unwrap_errors(list(validation_errors))
        if error.validator not in COMPLEX_VALIDATORS
    ]
    return sorted(set(check_errors))

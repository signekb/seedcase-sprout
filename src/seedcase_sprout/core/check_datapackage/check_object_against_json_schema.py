from jsonschema import Draft7Validator, FormatChecker

from seedcase_sprout.core.check_datapackage.check_error import CheckError
from seedcase_sprout.core.check_datapackage.validation_errors_to_check_errors import (
    validation_errors_to_check_errors,
)


def check_object_against_json_schema(
    json_object: dict, schema: dict
) -> list[CheckError]:
    """Checks that `json_object` matches the given JSON schema.

    Structural, type and format constraints are all checked. All schema violations are
    collected before errors are returned.

    Args:
        json_object: The JSON object to check.
        schema: The JSON schema to check against.

    Returns:
        A list of errors. An empty list, if no errors are found.

    Raises:
        jsonschema.exceptions.SchemaError: If the given schema is invalid.
    """
    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    return validation_errors_to_check_errors(validator.iter_errors(json_object))

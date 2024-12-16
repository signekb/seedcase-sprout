from jsonschema import Draft7Validator, FormatChecker, ValidationError


def check_object_against_json_schema(
    json_object: dict, schema: dict
) -> list[ValidationError]:
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
    return list(validator.iter_errors(json_object))

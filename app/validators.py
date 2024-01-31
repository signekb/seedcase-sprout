from django.core.validators import RegexValidator
from django.forms import ValidationError


from app.models import TableMetadata


def validate_no_special_characters(
    field_name: str, field_value: str
) -> ValidationError | None:
    """
    validate_no_special_characters checks that a field does not include
    special characters, i.e., characters that are not considered numbers or letters

    Args:
        field_name (str): Name of the field that should be included in the error message
        value (str): Field value which will be evaluated with the validator

    Returns:
        ValidationError | None: Returns validation error, if validation fails
    """

    validator = RegexValidator(
        regex=r"^[-a-zA-Z0-9_]+$",
        message=f"Please provide a {field_name} without special characters",
        code="invalid_value_special_characters",
    )
    return validator(field_value)


def validate_table_name_does_not_exist(name: str) -> ValidationError | None:
    """
    validate_table_name_does_not_exist checks whether a table with the given
    name does not exist in the database

    Args:
        name (Str): Table name

    Raises:
        ValidationError: If a table with the name already exists

    Returns:
        ValidationError | None: Returns validation error, if validation fails
    """

    if TableMetadata.objects.filter(name=name).exists():
        raise ValidationError(
            message="A table with this name already exists. Please provide another name.",
            code="invalid_table_name_already_exists",
        )

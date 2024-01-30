from django.core.validators import RegexValidator
from django import forms


from app.models import TableMetadata

def validate_no_special_characters(field_name: str, field_value: str):

    validator = RegexValidator(
        regex=r"^[-a-zA-Z0-9_]+$",
        message=f"Please provide a {field_name} without special characters",
        code="invalid_value_special_characters",
    )
    validator(field_value)


def validate_table_name_does_not_exist(name: str):
    """
    validate_table_name_does_not_exist checks whether a table with the given
    name does not exist in the database

    Args:
        name (Str): Table name

    Raises:
        forms.ValidationError: If a table with the name already exists
    """
    if TableMetadata.objects.filter(name=name).exists():
        raise forms.ValidationError(
            "A table with this name already exists. Please provide another name."
        )

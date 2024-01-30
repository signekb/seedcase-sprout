from django.core.validators import RegexValidator
from django import forms

from app.models import TableMetadata


def validate_no_special_characters(field_name: str):
    return RegexValidator(
        regex=r"^[-a-zA-Z0-9_]+$",
        message=f"Please provide a {field_name} without special characters",
        code="invalid_value_special_characters",
    )


def validate_table_name_does_not_exist(name):
    if TableMetadata.objects.filter(name=name).exists():
        raise forms.ValidationError(
            "A table with this name already exists. Please provide another name."
        )

"""This script contains field validators that can be included in the validator parameter
when defining fields in a model."""

from django.core.validators import RegexValidator
from django import forms

from app.models import TableMetadata

validate_no_special_characters = RegexValidator(
    regex=r"^[-a-zA-Z0-9_]+$",
    message="Please provide a value without special characters",
)


def validate_table_name_already_exists(name):
    if TableMetadata.objects.filter(name=name).exists():
        raise forms.ValidationError(
            "A table with this name already exists. Please provide another name."
        )

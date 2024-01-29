"""This script contains field validators that can be included in the validator parameter
when defining fields in a model."""

from django.core.validators import RegexValidator

does_field_include_special_characters = RegexValidator(
    regex=r"^[-a-zA-Z0-9_]+$",
    message="Must only include a-z, A-Z, 0-9, hyphens (-) and underscores (_)",
)

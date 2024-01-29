"""This script contains field validators that can be included in the validator parameter
when defining fields in a model."""

from django.core.validators import RegexValidator

validate_no_special_characters = RegexValidator(
    regex=r"^[-a-zA-Z0-9_]+$",
    message="Name must not contain special characters",
)

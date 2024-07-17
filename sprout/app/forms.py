"""Module defining forms."""

from django.forms import BooleanField, CharField, ModelForm, Textarea

from sprout.app.models import Columns, Tables
from sprout.app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class TablesForm(ModelForm):
    """ModelForm for creating Tables."""

    class Meta:
        """A class required by Django in a ModelForm.

        Defines which model is used and which fields that are included.
        """

        model = Tables
        fields = ["name", "description"]

        # Adding 'autocomplete: new-password' to disable suggestions on input field
        # TODO: Look into other solutions for this? (later)
        widgets = {
            "name": Textarea(attrs={"autocomplete": "new-password"}),
        }

    def clean_name(self) -> str:
        """Clean and validate field name.

        Adds extra validations for the field "name" on top of the validations
        defined by the model.

        Raises:
            ValidatorError: If either table name exists in the database or the name
            includes special characters.

        Returns:
            str: The cleaned value of the "name" field.
        """
        name_value = self.cleaned_data.get("name")

        validate_table_name_does_not_exist(name=name_value)

        validate_no_special_characters(field_name="name", field_value=name_value)

        return name_value


class ColumnsForm(ModelForm):
    """Based on the model Columns.

    The form is used to display and edit the content of
    the user-generated tables based on data from uploaded csv files.


    Args:
        ModelForm (ModelForm): pulled in from django.forms
    """

    description = CharField()
    excluded = BooleanField(initial=False, required=False)

    class Meta:  # noqa: D106
        model = Columns
        fields = (
            "machine_readable_name",
            "display_name",
            "description",
            "data_type",
            "allow_missing_value",
            "allow_duplicate_value",
        )

    def __init__(self, *args, **kwargs):
        """Overriding the __init__ method."""
        super().__init__(*args, **kwargs)

        self.fields["data_type"].empty_label = None
        # .empty_label removes the argument None from data_type, this could also be done
        # in the settings.py file if we would like to make it global.

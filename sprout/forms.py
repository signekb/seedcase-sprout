"""Module defining forms."""

from django.forms import CharField, ModelForm, Textarea

from sprout.models import ColumnMetadata, TableMetadata
from sprout.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class TableMetadataForm(ModelForm):
    """ModelForm for creating TableMetaData."""

    class Meta:
        """A class required by Django in a ModelForm.

        Defines which model is used and which fields that are included.
        """

        model = TableMetadata
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


class ColumnMetadataForm(ModelForm):
    """Based on the model ColumnMetaData.

    The form is used in column-review to display and edit the content of
    the user-generated tables based on data from uploaded csv files.


    Args:
        ModelForm (ModelForm): pulled in from django.forms
    """

    description = CharField()

    class Meta:  # noqa: D106
        model = ColumnMetadata
        fields = (
            "id",
            "original_name",
            "name",
            "title",
            "description",
            "data_type",
            "allow_missing_value",
            "allow_duplicate_value",
        )

    def __init__(self, *args, **kwargs):
        """Uses the Field.disabled to prevent editing of original_name."""
        super().__init__(*args, **kwargs)
        self.fields["original_name"].disabled = True
        # Disabling the original_name creates some problems in our tests as the field
        # is registered as missing. Solving this issue is discussed here:
        # https://stackoverflow.com/questions/4662848
        if kwargs.get("data"):
            self.initial = kwargs.get("data")

"""Module defining the forms."""

from app.models.table_metadata import TableMetadata
from app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class TableMetadataForm(ModelForm):
    """ModelForm for creating TableMetaData."""

    class Meta:
        """A class required by Django in a ModelForm.

        Describes which model to use and which fields to include.
        """

        model = TableMetadata
        fields = ["name", "description"]

    def clean_name(self) -> ValidationError | str:
        """clean_name Clean and validate field name.

        Adds extra validations for the field "name" on top of the validations
        defined by the model.

        Returns:
            ValidationError | str: name_value if validation is successful.
        """
        name_value = self.cleaned_data.get("name")

        # val: table name should not already exist in the db
        validate_table_name_does_not_exist(name=name_value)

        # val: table name should not contain special characters
        validate_no_special_characters(
            field_name="name", field_value=name_value
        )

        return name_value

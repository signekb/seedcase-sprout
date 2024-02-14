"""Module defining forms."""
from django.forms import ModelForm
from app.models import ColumnDataType, ColumnMetadata, TableMetadata
from app.models.table_metadata import TableMetadata
from app.validators import (
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


class ColumnDataTypeForm(ModelForm):
    """Form based on the model ColumnDataType.

    The form is used in columndata-review to display all info on data types.

    Args:
        ModelForm (ModelForm): pulled in from django.forms
    """

    class Meta:  # noqa: D106
        model = ColumnDataType
        fields = ["display_name", "description"]


class ColumnMetadataForm(ModelForm):
    """Based on the model ColumnMetaData.

    The form is used in column-review to display and edit the content of
    the user-generated tables based on data from uploaded csv files.


    Args:
        ModelForm (ModelForm): pulled in from django.forms
    """

    class Meta:  # noqa: D106
        model = ColumnMetadata
        fields = (
            "id",
            "table_metadata",
            "name",
            "title",
            "description",
            "data_type",
            "allow_missing_value",
            "allow_duplicate_value",
        )

from django import forms

from app.models import TableMetadata
from app.validators import (
    validate_no_special_characters,
    validate_table_name_already_exists,
)


class TableMetadataForm(forms.ModelForm):
    class Meta:
        model = TableMetadata
        fields = ["name", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")

        # If a table name already exists in the db, raise a validation error
        validate_table_name_already_exists(name=name)

        # If name contains special characters, raise validation error
        validate_no_special_characters(name)

        # If the name is unique, return the cleaned data
        return name

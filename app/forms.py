from django import forms

from app.models import TableMetadata
from app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class TableMetadataForm(forms.ModelForm):
    class Meta:
        model = TableMetadata
        fields = ["name", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")

        # If a table name already exists in the db, raise a validation error
        validate_table_name_does_not_exist(name=name)

        val_no_special_characters = validate_no_special_characters(field_name="name")
        val_no_special_characters(name)

        return name

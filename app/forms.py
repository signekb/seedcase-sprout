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

        # val: table name should not already exists in the db
        validate_table_name_does_not_exist(name=name)

        # val: table name should not contain special characters
        # define field_name for error msg
        val_no_special_characters = validate_no_special_characters(field_name="name")
        # run validator
        val_no_special_characters(name)

        return name

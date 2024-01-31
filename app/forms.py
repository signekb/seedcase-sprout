from django.forms import ModelForm, ValidationError

from app.models import TableMetadata
from app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class TableMetadataForm(ModelForm):
    class Meta:
        model = TableMetadata
        fields = ["name", "description"]

    def clean_name(self) -> ValidationError | str:
        """
        clean_name adds extra validations for the field "name" on top of
        the validations defined by the model

        Returns:
            ValidationError | str: name_value if validation is successful
        """

        name_value = self.cleaned_data.get("name")

        # val: table name should not already exists in the db
        validate_table_name_does_not_exist(name=name_value)

        # val: table name should not contain special characters
        validate_no_special_characters(field_name="name", field_value=name_value)

        return name_value

from django import forms

from app.models import TableMetadata


class TableMetadataForm(forms.ModelForm):
    class Meta:
        model = TableMetadata
        fields = ["name", "description"]


    def clean_name(self):
        name = self.cleaned_data.get("name")

        # Check if a table with the same name already exists
        existing_table = TableMetadata.objects.filter(name=name).exclude(pk=self.instance.pk).exists()

        # If a table with the same name exists, raise a validation error
        if existing_table:
            raise forms.ValidationError("A table with this name already exists. Please provide another name.")

        # If the name is unique, return the cleaned data
        return name
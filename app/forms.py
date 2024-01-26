from django import forms

from app.models import TableMetadata


class TableMetadataForm(forms.ModelForm):
    class Meta:
        model = TableMetadata
        fields = ["name", "description"]

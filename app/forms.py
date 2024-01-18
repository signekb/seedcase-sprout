from django import forms


class TableCreationForm(forms.Form):
    table_name = forms.CharField(label="table_name", max_length=200)
    table_description = forms.TextField(label="table_description")
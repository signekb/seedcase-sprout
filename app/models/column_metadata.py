"""Module defining the ColumnMetadata model."""
from django.db import models

from app.models.column_data_type import ColumnDataType
from app.models.table_metadata import TableMetadata


class ColumnMetadata(models.Model):
    """Model representing the metadata of columns."""

    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.ForeignKey(ColumnDataType, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()

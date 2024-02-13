"""File with ColumnMetadata."""
from django.db import models

from app.models.column_data_type import ColumnDataType
from app.models.table_metadata import TableMetadata


class ColumnMetadata(models.Model):
    """The metadata for a dataset column"""

    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.ForeignKey(ColumnDataType, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()

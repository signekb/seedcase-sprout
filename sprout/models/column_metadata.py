"""Module defining the ColumnMetadata model."""
import polars
from django.db import models

from sprout.models.column_data_type import ColumnDataType
from sprout.models.table_metadata import TableMetadata


class ColumnMetadata(models.Model):
    """Model representing the metadata of columns."""

    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    data_type = models.ForeignKey(ColumnDataType, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()

    @staticmethod
    def create(table_id: int, series: polars.Series) -> "ColumnMetadata":
        """Create ColumnMetadata from polars.Series.

        Args:
            table_id: id of the table
            series: A polars series

        Returns:
            ColumnMetadata: ColumnMetadata instance based on series
        """
        return ColumnMetadata(
            table_metadata_id=table_id,
            original_name=series.name,
            name=series.name,
            title=series.name,
            description="",
            data_type=ColumnDataType.get_from_series(series),
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

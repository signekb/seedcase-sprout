"""Module defining the Columns model."""

import polars
from django.db import models

from sprout.app.models.data_types import DataTypes
from sprout.app.models.tables import Tables
from sprout.core.utils import convert_to_human_readable, convert_to_snake_case


class Columns(models.Model):
    """Model representing the metadata of columns."""

    tables = models.ForeignKey(Tables, on_delete=models.CASCADE)
    extracted_name = models.CharField(max_length=1000)
    machine_readable_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    data_type = models.ForeignKey(DataTypes, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()

    @staticmethod
    def create(table_id: int, series: polars.Series) -> "Columns":
        """Create Columns from polars.Series.

        Args:
            table_id: id of the table
            series: A polars series

        Returns:
            Columns: Columns instance based on series
        """
        return Columns(
            tables_id=table_id,
            extracted_name=series.name,
            machine_readable_name=convert_to_snake_case(series.name),
            display_name=convert_to_human_readable(series.name),
            description="",
            data_type=DataTypes.get_from_series(series),
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

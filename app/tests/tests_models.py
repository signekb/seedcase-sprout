"""Tests for models."""
import datetime

from django.test import TestCase
from polars import Series

from app.models import ColumnDataType, ColumnMetadata, TableMetadata
from app.tests.db_test_utils import create_metadata_table_and_column


class MetadataTests(TestCase):
    """Tests for metadata models.

    This includes TableMetadata and ColumnMetadata.
    """

    def test_create_metadata_for_a_table_and_columns_and_verify_creation(self):
        """Test for the creation of metadata.

        Tests that a table and a column exist in the database after creation
        """
        # Arrange
        table_name = "TableName"
        column_name = "ColumnName"
        create_metadata_table_and_column(table_name, column_name)

        # Act
        table_exists = TableMetadata.objects.filter(name=table_name).exists()
        column_exists = ColumnMetadata.objects.filter(name=column_name).exists()

        # Assert
        self.assertTrue(table_exists, "Table metadata should be created")
        self.assertTrue(column_exists, "Column metadata should be created")

    def test_key_constraint_should_delete_column_if_table_deleted(self):
        """Test of foreign Key constraint that should delete column when table deleted.

        Tests that when we delete a table, the column is also deleted.
        """
        # Arrange
        create_metadata_table_and_column()

        # Act
        TableMetadata.objects.first().delete()

        # Assert
        self.assertEqual(0, TableMetadata.objects.count(), "Table should be deleted")
        self.assertEqual(0, ColumnMetadata.objects.count(), "Column should be deleted")

    def test_verify_table_is_not_deleted_when_column_is_deleted(self):
        """Test of column deletion not deleting table.

        Tests that when a column is deleted from a table, the table isn't deleted as
        well.
        """
        # Arrange
        create_metadata_table_and_column()

        # Act
        ColumnMetadata.objects.first().delete()

        # Assert
        table_count = TableMetadata.objects.count()
        self.assertEqual(1, table_count, "Table should not be deleted")
        column_count = ColumnMetadata.objects.count()
        self.assertEqual(0, column_count, "Column should be deleted")


class ColumnDataTypeTests(TestCase):
    """Tests for ColumnDataType."""

    def test_get_from_series_Whole_Number(self):
        """get_from_series should return 'Whole Number' for int series."""
        series_int = Series([1])

        column_data_type = ColumnDataType.get_from_series(series_int)

        self.assertEqual("Whole Number", column_data_type.display_name)

    def test_get_from_series_Decimal(self):
        """get_from_series should return 'Decimal' for float series."""
        series_decimal = Series([1.1])

        column_data_type = ColumnDataType.get_from_series(series_decimal)

        self.assertEqual("Decimal", column_data_type.display_name)

    def test_get_from_series_YesOrNo(self):
        """get_from_series should return 'Yes/No' for boolean series."""
        series_bool = Series([True])

        column_data_type = ColumnDataType.get_from_series(series_bool)

        self.assertEqual("Yes/No", column_data_type.display_name)

    def test_get_from_series_Text(self):
        """get_from_series should return 'Text' for string series."""
        series_string = Series(["Hello"])

        column_data_type = ColumnDataType.get_from_series(series_string)

        self.assertEqual("Text", column_data_type.display_name)

    def test_get_from_series_Time(self):
        """get_from_series should return 'Time' for time series."""
        series_time = Series([datetime.time(1, 2, 3)])

        column_data_type = ColumnDataType.get_from_series(series_time)

        self.assertEqual("Time", column_data_type.display_name)

    def test_get_from_series_Date(self):
        """get_from_series should return 'Date' for date series."""
        series_date = Series([datetime.date(2024, 2, 3)])

        column_data_type = ColumnDataType.get_from_series(series_date)

        self.assertEqual("Date", column_data_type.display_name)

    def test_get_from_series_DatePlusTime(self):
        """get_from_series should return 'Date+Time' for datetime series."""
        series_datetime = Series([datetime.datetime(2024, 2, 3)])

        column_data_type = ColumnDataType.get_from_series(series_datetime)

        self.assertEqual("Date+Time", column_data_type.display_name)

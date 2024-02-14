"""Tests for models."""
from django.test import TestCase

from app.models import ColumnMetadata, TableMetadata
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

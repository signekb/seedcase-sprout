"""Tests for models."""

from django.test import TestCase

from sprout.models import Columns, Tables
from sprout.tests.db_test_utils import create_metadata_table_and_column, create_table


class TableAndColumnsTests(TestCase):
    """Tests for metadata models.

    This includes Tables and Columns.
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
        table_exists = Tables.objects.filter(name=table_name).exists()
        column_exists = Columns.objects.filter(
            machine_readable_name=column_name
        ).exists()

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
        Tables.objects.first().delete()

        # Assert
        self.assertEqual(0, Tables.objects.count(), "Table should be deleted")
        self.assertEqual(0, Columns.objects.count(), "Column should be deleted")

    def test_verify_table_is_not_deleted_when_column_is_deleted(self):
        """Test of column deletion not deleting table.

        Tests that when a column is deleted from a table, the table isn't deleted as
        well.
        """
        # Arrange
        create_metadata_table_and_column()

        # Act
        Columns.objects.first().delete()

        # Assert
        table_count = Tables.objects.count()
        self.assertEqual(1, table_count, "Table should not be deleted")
        column_count = Columns.objects.count()
        self.assertEqual(0, column_count, "Column should be deleted")

    def test_modified_at_should_be_null_on_creation(self):
        # Arrange
        table_name = "TestTable"
        table = create_table(table_name)
        table.save()
        initial_modified_at = table.modified_at

        # Assert
        self.assertIsNone(initial_modified_at, "modified_at should be null")

    def test_modified_at_should_be_updated_on_save(self):
        # Arrange
        table_name = "TestTable"
        table = create_table(table_name)
        table.save()
        initial_modified_at = table.modified_at

        # Act
        table.name = "A change"
        table.save()

        # Assert
        self.assertNotEqual(
            initial_modified_at, table.modified_at, "modified_at should be updated"
        )
        self.assertIsNotNone(table.modified_at, "modified_at should NOT be null")

    def test_data_rows_should_be_zero_on_creation(self):
        # Arrange
        table_name = "TestTable"
        table = create_table(table_name)
        table.save()

        # Assert
        self.assertEqual(0, table.data_rows, "data_rows should be zero")


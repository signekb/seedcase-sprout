from django.test import TestCase
from app.models import TableMetadata, ColumnMetadata
from app.tests.db_test_utils import create_metadata_table_and_column


class MetadataTests(TestCase):

    def test_create_metadata_for_a_table_and_columns_and_verify_creation(self):
        # Arrange
        create_metadata_table_and_column()

        # Act
        table_count = TableMetadata.objects.count()
        column_count = ColumnMetadata.objects.count()

        # Assert
        self.assertEqual(1, table_count, "Table metadata should be created")
        self.assertEqual(1, column_count, "Column metadata should be created")

    def test_verify_foreign_key_constraint_by_deleting_table_which_should_delete_column(self):
        # Arrange
        create_metadata_table_and_column()

        # Act
        TableMetadata.objects.first().delete()

        # Assert
        self.assertEqual(0, TableMetadata.objects.count(), "Table should be deleted")
        self.assertEqual(0, ColumnMetadata.objects.count(), "Column should be deleted")

    def test_verify_table_is_not_deleted_when_column_is_deleted(self):
        # Arrange
        create_metadata_table_and_column()

        # Act
        ColumnMetadata.objects.first().delete()

        # Assert
        self.assertEqual(1, TableMetadata.objects.count(), "Table should not be deleted")
        self.assertEqual(0, ColumnMetadata.objects.count(), "Column should be deleted")



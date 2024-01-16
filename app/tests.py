from django.test import TestCase
from app.models import TableMetadata, ColumnMetadata, ColumnDataType


class MetadataTests(TestCase):

    def test_create_metadata_for_a_table_and_columns_and_verify_creation(self):
        # Arrange
        self.create_metadata_table_and_column()

        # Act
        table_count = TableMetadata.objects.count()
        column_count = ColumnMetadata.objects.count()

        # Assert
        self.assertEqual(1, table_count, "Table metadata should be created")
        self.assertEqual(1, column_count, "Column metadata should be created")

    def test_verify_foreign_key_constraint_by_deleting_table_which_should_delete_column(self):
        # Arrange
        self.create_metadata_table_and_column()

        # Act
        TableMetadata.objects.first().delete()

        # Assert
        self.assertEqual(0, TableMetadata.objects.count(), "Table should be deleted")
        self.assertEqual(0, ColumnMetadata.objects.count(), "Column should be deleted")

    @staticmethod
    def create_metadata_table_and_column():
        table_metadata = TableMetadata(name="TestTable",
                                       original_file_name="test_file.csv",
                                       description="Table create for testing",
                                       created_by=1)
        table_metadata.save()

        column_data_type = ColumnDataType(display_name="Text")
        column_data_type.save()

        column = ColumnMetadata(table_metadata=table_metadata, name="ColumnName",
                                title="Friendly Column Name",
                                description="Description of column",
                                data_type=column_data_type,
                                allow_missing_value=True,
                                allow_duplicate_value=True)
        column.save()

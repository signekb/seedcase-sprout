"""Tests for the project id data view."""

import io

from django.test import TestCase
from django.urls import reverse

from sprout.models import ColumnMetadata, FileMetadata, TableMetadata
from sprout.tests.db_test_utils import create_table


class ProjectIdMetaDataTests(TestCase):
    """Tests for the file upload view."""

    def setUp(self):
        """Create a table and a column for testing."""
        self.table_metadata = TableMetadata.objects.create(
            name="Test Table",
            description="Test table description.",
        )
        self.column_metadata = ColumnMetadata.objects.create(
            table_metadata=self.table_metadata,
            extracted_name="TestColumn",
            machine_readable_name="test_column",
            display_name="Test Column",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C")
        file.name = "file-name.csv"
        self.file_metadata = FileMetadata.create_file_metadata(
            file, self.table_metadata.pk
        )

    def test_view_renders(self):
        """Test that the get function renders."""
        # Arrange
        url = reverse("project-id-metadata-view")

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project-id-metadata-view.html")

    def test_view_shows_all_tables(self):
        """Test that the view shows all tables in TableMetadata."""
        # Arrange
        url = reverse("project-id-metadata-view")
        create_table("Table1").save()
        create_table("Table2").save()
        tables = TableMetadata.objects.all()

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        for table in tables:
            self.assertContains(response, table.name)

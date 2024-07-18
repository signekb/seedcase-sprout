"""Tests for the project id data view."""

import io

from django.test import TestCase
from django.urls import reverse

from sprout.app.models import Columns, Files, Tables
from tests.db_test_utils import create_table


class ProjectIdMetaDataTests(TestCase):
    """Tests for the file upload view."""

    def setUp(self):
        """Create a table and a column for testing."""
        self.tables = Tables.objects.create(
            name="Test Table",
            description="Test table description.",
        )
        self.columns = Columns.objects.create(
            tables=self.tables,
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
        self.files = Files.create_model(file, self.tables.pk)

        self.url = reverse("projects-id-metadata-view")

    def test_view_renders(self):
        """Test that the get function renders."""
        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects-id-metadata-view.html")

    def test_view_shows_all_tables(self):
        """Test that the view shows all tables in Tables."""
        # Arrange
        create_table("Table1").save()
        create_table("Table2").save()
        tables = Tables.objects.all()

        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        for table in tables:
            self.assertContains(response, table.name)

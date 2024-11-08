import io
import os

from django.test import TestCase

from seedcase_sprout.app.models import Columns, Files, Tables
from seedcase_sprout.app.views.projects_id_metadata_id.helpers import create_stepper_url
from seedcase_sprout.app.views.projects_id_metadata_id.step_columns import (
    create_sample_of_unique_values,
)


class MetadataIDUpdateViewTest(TestCase):
    """Test for the Data Metadata update (as table) page."""

    def setUp(self):
        """Create a table and a column for testing."""
        self.table = Tables.objects.create(
            name="Test Table",
            description="Test table description.",
        )
        self.column = Columns.objects.create(
            tables=self.table,
            extracted_name="TestColumn",
            machine_readable_name="test_column",
            display_name="Test Display Name",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C\n4,C\n5,C\n6,C")
        file.name = "file-name.csv"
        self.file = Files.create_model(file, self.table.id)
        self.current_url = create_stepper_url(3, table_id=self.table.id)
        self.redirect_url = create_stepper_url(4, table_id=self.table.id)

    def test_projects_id_metadata_id_update_view_get(self):
        """Test that the get function works."""
        # Act
        response = self.client.get(self.current_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects-id-metadata-create.html")

    def test_projects_id_metadata_id_update_view_post_valid_data(self):
        """Test that the view works if valid data is entered."""
        # Arrange
        data = {
            f"{self.column.id}-machine_read_name": "Updated Machine-Read Name",
            f"{self.column.id}-display_name": "Updated Column Display Name",
            f"{self.column.id}-description": "Test Description",
            f"{self.column.id}-data_type": 0,
            f"{self.column.id}-allow_missing_value": True,
            f"{self.column.id}-allow_duplicate_value": False,
        }

        # Act
        response = self.client.post(self.current_url, data, follow=True)

        # Assert the status code
        self.assertRedirects(response, self.redirect_url)

    def test_create_sample_of_unique_values(self):
        """Test if correct sample values are created."""
        tables_id = self.table.id

        sample = create_sample_of_unique_values(tables_id)

        self.assertEqual([1, 2, 3, 4, 5], sample["TestColumn"])
        self.assertEqual(["A", "B", "C"], sample["Letter"])

    def test_excluded_should_delete_column(self):
        """An excluded column should be removed even if form is not valid."""
        # Arrange
        data = {
            f"{self.column.id}-excluded": True,
        }

        # Act
        response = self.client.post(self.current_url, data, follow=True)

        # Assert the status code
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Columns.objects.filter(id=self.column.id).exists())

    def tearDown(self):
        os.remove(self.file.server_file_path)

import io
import os

from django.test import TestCase
from django.urls import reverse

from sprout.models import Columns, Files, Tables
from sprout.views.projects_id_metadata_id_update import create_sample_of_unique_values


class MetadataIDUpdateViewTest(TestCase):
    """Test for the Data Metadata update (as table) page."""

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
            display_name="Test Display Name",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C\n4,C\n5,C\n6,C")
        file.name = "file-name.csv"
        self.files = Files.create_model(file, self.tables.id)

    def test_projects_id_metadata_id_update_view_get(self):
        """Test that the get function works."""
        # Arrange
        url = reverse("projects-id-metadata-id-update", args=[self.tables.id])

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects-id-metadata-id-update.html")

    def test_projects_id_metadata_id_update_view_post_valid_data(self):
        """Test that the view works if valid data is entered."""
        # Arrange
        url = reverse("projects-id-metadata-id-update", args=[self.tables.id])
        data = {
            f"{self.columns.id}-machine_read_name": "Updated Machine-Read Name",
            f"{self.columns.id}-display_name": "Updated Column Display Name",
            f"{self.columns.id}-description": "Test Description",
            f"{self.columns.id}-data_type": 0,
            f"{self.columns.id}-allow_missing_value": True,
            f"{self.columns.id}-allow_duplicate_value": False,
        }

        # Act
        response = self.client.post(url, data, follow=True)

        # Assert the status code
        self.assertRedirects(response, reverse("projects-id-metadata-view"))

    def test_create_sample_of_unique_values(self):
        """Test if correct sample values are created."""
        tables_id = self.tables.id

        sample = create_sample_of_unique_values(tables_id)

        self.assertEqual([1, 2, 3, 4, 5], sample["TestColumn"])
        self.assertEqual(["A", "B", "C"], sample["Letter"])

    def test_excluded_should_delete_column(self):
        """An excluded column should be removed even if form is not valid."""
        # Arrange
        url = reverse("projects-id-metadata-id-update", args=[self.tables.id])
        data = {
            f"{self.columns.id}-excluded": True,
        }

        # Act
        response = self.client.post(url, data, follow=True)

        # Assert the status code
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Columns.objects.filter(id=self.columns.id).exists())

    def tearDown(self):
        os.remove(self.files.server_file_path)

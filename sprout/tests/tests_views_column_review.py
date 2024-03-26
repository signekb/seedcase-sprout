"""Tests for views."""

import io
import os

from django.test import TestCase
from django.urls import reverse

from sprout.models import ColumnMetadata, FileMetadata, TableMetadata
from sprout.views.column_review import create_sample_of_unique_values


class ColumnReviewViewTest(TestCase):
    """Test for the Column Review page.

    This is where the uploaded metadata for columns are uploaded and edited.
    """

    def setUp(self):
        """Create a table and a column for testing."""
        self.table_metadata = TableMetadata.objects.create(
            name="Test Table",
            description="Test table description.",
        )
        self.column_metadata = ColumnMetadata.objects.create(
            table_metadata=self.table_metadata,
            name="Test Column",
            original_name="TestColumn",
            title="Test Title",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C\n4,C\n5,C\n6,C")
        file.name = "file-name.csv"
        self.file_metadata = FileMetadata.create_file_metadata(
            file, self.table_metadata.id
        )

    def test_column_review_view_get(self):
        """Test that the get function works."""
        # Arrange
        url = reverse("column-review", args=[self.table_metadata.id])

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "column-review.html")

    def test_column_review_view_post_valid_data(self):
        """Test of column-review page. Preview data is extracted from file, so it
        needs to be created too."""
        # Arrange

        url = reverse("column-review", args=[self.table_metadata.id])
        data = {
            f"{self.column_metadata.id}-name": "Updated Column Name",
            f"{self.column_metadata.id}-title": "Updated Column Title",
            f"{self.column_metadata.id}-description": "Test Description",
            f"{self.column_metadata.id}-data_type": 0,
            f"{self.column_metadata.id}-allow_missing_value": True,
            f"{self.column_metadata.id}-allow_duplicate_value": False,
        }

        # Act
        response = self.client.post(url, data, follow=True)

        # Assert the status code
        self.assertEqual(response.status_code, 200)

    def test_create_sample_of_unique_values(self):
        """Test if correct sample values are created."""
        table_metadata_id = self.table_metadata.id

        sample = create_sample_of_unique_values(table_metadata_id)

        self.assertEqual([1, 2, 3, 4, 5], sample["TestColumn"])
        self.assertEqual(["A", "B", "C"], sample["Letter"])

    def tearDown(self):
        os.remove(self.file_metadata.server_file_path)

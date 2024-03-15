"""Tests for views."""

from django.test import TestCase
from django.urls import reverse

from sprout.models import ColumnMetadata, TableMetadata


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
            title="Test Title",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

    def test_column_review_view_get(self):
        """Test that the get function works."""
        # Arrange
        url = reverse(
            "project-id-data-id-metadata-edit-grid", args=[self.table_metadata.id]
        )

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project-id-data-id-metadata-edit-grid.html")

    def test_column_review_view_post_valid_data(self):
        """Test that the view works if valid data is entered."""
        # Arrange
        url = reverse(
            "project-id-data-id-metadata-edit-grid", args=[self.table_metadata.id]
        )
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

"""Tests for the metadata create view."""

from django.test import TestCase
from django.urls import reverse

from sprout.models import TableMetadata
from sprout.tests.db_test_utils import create_table


class ProjectIdDataTests(TestCase):
    """Tests for the file upload view."""

    def test_view_renders(self):
        """Test that the get function renders."""
        # Arrange
        url = reverse("project_id_data")

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project-id-data.html")

    def test_view_shows_all_tables(self):
        """Test that the view shows all tables in TableMetadata."""
        # Arrange
        url = reverse("project_id_data")
        create_table("Table1").save()
        create_table("Table2").save()
        tables = TableMetadata.objects.all()

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        for table in tables:
            self.assertContains(response, table.name)


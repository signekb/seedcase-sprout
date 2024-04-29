"""Tests for the data import view."""

from django.test import TestCase
from django.urls import reverse


class ProjectIDViewTests(TestCase):
    """Tests for the project landing page view."""

    url = reverse("projects-id-view")

    def test_projects_id_view_renders(self):
        """Test that the page renders."""
        # Arrange/Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects-id-view.html")

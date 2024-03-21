"""Tests for the project id data view."""

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

    def test_view_redirects_to_data_import_with_button_create(self):
        """Test that the post function redirects to data-import
        when button_create is clicked."""

        # Arrange
        url = reverse("project_id_data")

        # Act
        response = self.client.post(url, data={"button_create": "True"})

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("data_import"))

    def test_view_does_not_redirect_with_buttons_edit_upload_wo_selected_row(self):
        """Test that the post function does not redirect to column_review
        when button_edit is clicked without selected row and that msg is not None."""
        # Arrange
        url = reverse("project_id_data")

        # Act
        response_edit = self.client.post(url, data={"button_edit": "True"})
        response_upload = self.client.post(url, data={"button_upload": "True"})

        # Assert
        self.assertEqual(response_edit.status_code, 200)
        self.assertTemplateUsed(response_edit, "project-id-data.html")
        self.assertIsNotNone(response_edit.context["msg_edit_upload_wo_selected_row"])

        self.assertEqual(response_upload.status_code, 200)
        self.assertTemplateUsed(response_upload, "project-id-data.html")
        self.assertIsNotNone(response_upload.context["msg_edit_upload_wo_selected_row"])

    def test_view_redirects_with_button_edit_and_selected_row(self):
        """Test that the post function redirects to column_review
        when the 'button_edit' is clicked with a selected row.
        """
        # Arrange
        url = reverse("project_id_data")

        # Act
        response = self.client.post(
            url, data={"button_edit": "True", "selected_metadata_id": 1}, follow=True
        )
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("column-review", args=[1]))

    def test_view_redirects_with_button_upload_and_selected_row(self):
        """Test that the post function redirects to column_review
        when the 'button_upload' is clicked with a selected row.
        This is done separate to edit, since these will eventually
        redirect to different views.
        """
        # Arrange
        url = reverse("project_id_data")

        # Act
        response = self.client.post(
            url, data={"button_upload": "True", "selected_metadata_id": 1}, follow=True
        )

        # Assert
        self.assertRedirects(response, reverse("column-review", args=[1]))

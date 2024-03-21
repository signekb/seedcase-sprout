"""Tests for the project id data view."""
import io

from django.test import TestCase
from django.urls import reverse

from sprout.models import TableMetadata, ColumnMetadata, FileMetadata
from sprout.tests.db_test_utils import create_table


class ProjectIdDataTests(TestCase):
    """Tests for the file upload view."""
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

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C")
        file.name = "file-name.csv"
        self.file_metadata = FileMetadata.create_file_metadata(
            file, self.table_metadata.id
        )

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
        table_id = self.table_metadata.id
        url = reverse("project_id_data") + "?selected_metadata_id=" + str(table_id)

        # Act
        response = self.client.post(
            url, data={"button_upload": "True"}, follow=True
        )

        # Assert
        self.assertRedirects(
            response, "/column-review/1", status_code=302, target_status_code=200
        )
        # self.assertRedirects(response, reverse("column-review", args=[1]))

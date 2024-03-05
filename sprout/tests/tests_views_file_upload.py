"""Tests for the file upload view."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from sprout.models import TableMetadata
from sprout.tests.db_test_utils import create_table


class FileUploadTests(TestCase):
    """Tests for the file upload view."""

    def test_render_file_upload_view_and_verify_that_table_name_is_loaded(self):
        """Test for the view being loaded and table_name is present in view.

        Tests that the status code is 200 and that the html contains table_name
        """
        # Arrange
        table_name = "Table Name"
        create_table(table_name).save()

        # Act
        response = Client().get("/file-upload/1")

        # Assert.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, table_name)

    def test_upload_of_file_should_create_columns_in_database(self):
        """Test for a table being created when csv is uploaded."""
        # Arrange
        table_name = "Table Name"
        file_name = "file.csv"
        create_table(table_name).save()
        file = SimpleUploadedFile(file_name, b"first_name,second_name,age")

        # Act
        response = Client().post("/file-upload/1", {"uploaded_file": file})

        # Assert
        table = TableMetadata.objects.get(name=table_name)
        self.assertEqual("file.csv", table.original_file_name)
        self.assertEqual(302, response.status_code, "Redirect is expected")
        self.assertEqual("/column-review/1", response.url)
        self.assertEqual(3, table.columnmetadata_set.all().count(), "expects 3 columns")

    def test_upload_failed_with_wrong_file_extension(self):
        """Test for error message when file is not ending on .csv."""
        create_table("Table Name").save()
        file = SimpleUploadedFile("file-with-wrong-ext.svg", b"file content")

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unsupported file format: .svg")

    def test_upload_failed_with_invalid_csv_header(self):
        """Test for error if not able to extract headers from CSV."""
        create_table("Table Name").save()
        file = SimpleUploadedFile("file-with-bad-headers.csv", b"no valid headers")

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unable to extract column headers")

"""Tests for views."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from app.models import TableMetadata
from app.tests.db_test_utils import create_table


class DataImportTests(TestCase):
    """Tests for the data import view."""

    url = reverse("data_import")
    empty_form = {}
    invalid_form = {"name": "Test/Table", "description": "Test description"}
    valid_form = {"name": "TestTable", "description": "Test description"}

    def test_data_import_renders(self):
        """Test that data import renders.

        Tests that the page is rendered using the expected template, when the response
        method is "GET".
        """
        # Arrange/Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "data-import.html")

    def test_fields_are_required(self):
        """Test for when the required fields, name and description, are empty.

        Tests that the expected errors occur when the form is empty (i.e., "This field
        is required").
        """
        # Arrange/Act
        response = self.client.post(self.url, self.empty_form)

        # Assert
        self.assertFormError(response, "form", "name", "This field is required.")
        self.assertFormError(response, "form", "description", "This field is required.")

    def test_redirect_with_valid_form(self):
        """Test for redirect when the form is valid.

        Tests that the page is redirected when a valid form is submitted.
        """
        # Arrange/Act
        response = self.client.post(
            self.url,
            data=self.valid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, "/file-upload/1")
        # (the above will, hopefully, work when file-upload is implemented)

    def test_no_redirect_with_invalid_form_special_characters(self):
        """Test that no redirection when the "name" field contains special characters.

        Tests that the page isn't redirected when an invalid form with special
        characters in the "name" field is submitted.
        """
        # Arrange/Act
        response = self.client.post(
            self.url,
            data=self.invalid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_with_valid_form_table_exists(self):
        """Test that page isn't redirected when a table with the submitted name exists.

        Tests that page isn't redirected when a valid form with a table name that already
        exists in the database is submitted.
        """
        # Arrange
        TableMetadata.objects.create(name="TestTable", description="Test description")

        # Act
        response = self.client.post(
            self.url,
            data=self.valid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 200)


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
        self.assertEqual("/edit-table-columns/1", response.url)
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

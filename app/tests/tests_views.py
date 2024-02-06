from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from app.tests.db_test_utils import create_table

from django.test import TestCase
from django.urls import reverse

from app.models import TableMetadata


class DataImportTests(TestCase):
    url = reverse("data_import")
    empty_form = {}
    invalid_form = {"name": "Test/Table", "description": "Test description"}
    valid_form = {"name": "TestTable", "description": "Test description"}

    def test_data_import_renders(self):
        """test_data_import_renders Check that data import renders.

        Checks that tbe page is rendered using the expected template, when the
        response method is "GET".
        """
        # Arrange/Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "data-import.html")

    def test_fields_are_required(self):
        """test_fields_are_required Check required fields.

        Checks that the expected errors occur when the form is empty (i.e.,
        "This field is required").
        """
        # Arrange/Act
        response = self.client.post(self.url, self.empty_form)

        # Assert
        self.assertFormError(
            response, "form", "name", "This field is required."
        )
        self.assertFormError(
            response, "form", "description", "This field is required."
        )

    def test_redirect_with_valid_form(self):
        """test_redirect_with_valid_form Check for redirect.

        Checks that the page is redirected when a valid form is submitted.
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
        """test_no_redirect_with_invalid_form_special_characters Check for correctly no redirecting.

        Checks that the page isn't redirected when an invalid form with special
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
        """test_no_redirect_with_valid_form_table_exists Check that page isn't redirected.

        Checks that page isn't redirected when a valid form with a table name
        that already exists in the database is submitted.
        """
        # Arrange
        TableMetadata.objects.create(
            name="TestTable", description="Test description"
        )

        # Act
        response = self.client.post(
            self.url,
            data=self.valid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 200)


class FileUploadTests(TestCase):
    def test_render_file_upload_view_and_verify_that_table_metadata_is_loaded(
        self,
    ):
        # Arrange
        table_name = "Table Name"
        create_table(table_name).save()

        # Act
        response = Client().get("/file-upload/1")

        # Assert. assertContains checks if status_code=200 and
        # html should contain table_name
        self.assertContains(response, table_name)

    def test_upload_of_file_should_create_columns_in_database(self):
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
        self.assertEqual(
            3, table.columnmetadata_set.all().count(), "expects 3 columns"
        )

    def test_upload_failed_with_wrong_file_extension(self):
        create_table("Table Name").save()
        file = SimpleUploadedFile("file-with-wrong-ext.svg", b"file content")

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unsupported file format: .svg")

    def test_upload_failed_with_invalid_csv_header(self):
        create_table("Table Name").save()
        file = SimpleUploadedFile(
            "file-with-bad-headers.csv", b"no valid headers"
        )

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unable to extract column headers")

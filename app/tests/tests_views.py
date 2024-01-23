from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client

from app.models import ColumnMetadata
from app.tests.db_test_utils import create_table


class FileUploadTests(TestCase):
    def test_render_file_upload_view_and_verify_that_table_is_loaded(self):
        # Arrange
        table_name = "Table Name"
        create_table(table_name).save()

        # Act
        response = Client().get("/file-upload/1")

        # Assert. assertContains checks if status_code=200 and
        # html should contain "TestTable"
        self.assertContains(response, table_name)

    def test_upload_of_file_should_create_columns_in_database(self):
        # Arrange
        table_name = "Table Name"
        create_table(table_name).save()
        file = SimpleUploadedFile("file.csv", b"first_name,second_name,age")

        # Act
        response = Client().post("/file-upload/1", {"uploaded_file": file})

        # Assert
        self.assertEqual(302, response.status_code, "Redirect is expected")
        self.assertEqual("/edit-table-columns/1", response.url)
        columns = ColumnMetadata.objects.all()
        self.assertEqual(3, columns.count(), "Three columns are created")

    def test_upload_failed_with_wrong_file_extension(self):
        create_table("Table Name").save()
        file = SimpleUploadedFile("file-with-wrong-ext.svg", b"file content")

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unsupported file format: .svg")

    def test_upload_failed_with_missing_file_error(self):
        create_table("Table Name").save()

        response = Client().post("/file-upload/1")

        self.assertContains(response, "The file is missing!")

    def test_upload_failed_with_invalid_csv_header(self):
        create_table("Table Name").save()
        file = SimpleUploadedFile("file-with-bad-headers.csv", b"no valid headers")

        response = Client().post("/file-upload/1", {"uploaded_file": file})

        self.assertContains(response, "Unable to extract column headers")

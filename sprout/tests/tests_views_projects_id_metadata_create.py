"""Tests for the metadata create view."""

import io
from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from sprout.models import ColumnMetadata, FileMetadata, TableMetadata
from sprout.tests.db_test_utils import create_table


class MetadataCreateTests(TestCase):
    """Tests for the file upload view."""

    def test_render_projects_id_metadata_create_view_and_verify_loaded_table_names(
        self,
    ):
        """Test for the view being loaded and table_name is present in view.

        Tests that the status code is 200 and that the html contains table_name
        """
        # Arrange
        table_name = "Table Name"
        create_table(table_name).save()

        # Act
        response = self.client.get("/metadata/1/create")

        # Assert.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, table_name)

    def test_upload_of_file_should_create_columns_in_database(self):
        """Test for a table being created when csv is uploaded."""
        # Arrange
        table_name = "Table"
        file_name = table_name + ".csv"
        create_table(table_name).save()
        file = self.create_file(file_name, "name,city,age\nPhil,Aarhus,36")

        # Act
        response = self.client.post("/metadata/1/create", {"uploaded_file": file})

        # Assert
        table = TableMetadata.objects.get(name=table_name)
        self.assertEqual("Table.csv", table.original_file_name)
        self.assertEqual(302, response.status_code, "Redirect is expected")
        self.assertEqual("/metadata/1/update", response.url)
        self.assertEqual(3, table.columnmetadata_set.all().count(), "expects 3 columns")
        # Clean up
        FileMetadata.objects.first().delete()

    def test_extracted_column_names_formats(self):
        """Test for a table being created when csv is uploaded."""
        # Arrange
        create_table("Table Name").save()

        file = self.create_file("file.csv", "DISPLAY_NAME,AGE\nPhil,36")

        # Act
        self.client.post("/metadata/create/1", {"uploaded_file": file})

        # Assert
        column = ColumnMetadata.objects.filter(extracted_name="DISPLAY_NAME").first()
        self.assertEqual("Display Name", column.display_name)
        self.assertEqual("display_name", column.machine_readable_name)
        # Clean up
        FileMetadata.objects.first().delete()

    def test_upload_failed_with_wrong_file_extension(self):
        """Test for error message when file is not ending on .csv."""
        create_table("Table Name").save()
        file = self.create_file("file-with-wrong-ext.svg", "file content")

        response = self.client.post("/metadata/1/create", {"uploaded_file": file})

        self.assertContains(response, "Unsupported file format: .svg")

    def test_upload_failed_with_no_rows_found(self):
        """Test for error if not able to extract headers from CSV."""
        create_table("Table Name").save()
        file = self.create_file("file-with-bad-headers.csv", "name, age")

        response = self.client.post("/metadata/1/create", {"uploaded_file": file})

        self.assertContains(response, "Invalid CSV. No rows found!")

    def test_resubmit_of_file_should_delete_prev_file_and_columns(self):
        """Resubmitting a file table should delete the previous file and columns."""
        # Arrange
        expected_file_content = "name,city,age\nPhil,Aarhus,36"
        table = create_table("Table Name")
        table.save()
        file1 = self.create_file("file.csv", "first_name,year\nHans,2000")
        file2 = self.create_file("file.csv", expected_file_content)
        url = reverse("projects-id-metadata-create", kwargs={"table_id": table.id})

        # Act
        self.client.post(url, {"uploaded_file": file1})
        self.client.post(url, {"uploaded_file": file2})

        # Assert
        files = FileMetadata.objects.all()
        columns = ColumnMetadata.objects.all()
        self.assertEqual(1, files.count())
        self.assertEqual(3, columns.count())

        expected_columns = ["name", "city", "age"]
        actual_columns = list(map(lambda c: c.extracted_name, columns))
        self.assertEqual(actual_columns, expected_columns)

        actual_file_content = Path(files.first().server_file_path).read_text()
        self.assertEqual(expected_file_content, actual_file_content)

        # Clean up
        FileMetadata.objects.first().delete()

    @staticmethod
    def create_file(name: str, content: str) -> io.BytesIO:
        """Create file for test."""
        file = io.BytesIO(content.encode("utf-8"))
        file.name = name
        return file

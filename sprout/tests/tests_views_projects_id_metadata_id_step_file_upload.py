import io
from pathlib import Path

from django.test import TestCase

from sprout.models import Columns, Files
from sprout.tests.db_test_utils import create_table
from sprout.views.projects_id_metadata_id.helpers import create_stepper_url


class MetadataStepFileUploadTests(TestCase):
    def setUp(self):
        """Called automatically by Django to prepare for a test."""
        self.table = create_table("Table")
        self.table.save()
        self.current_url = create_stepper_url(2, table_id=self.table.id)
        self.expected_redirect_url = create_stepper_url(3, table_id=self.table.id)

    def test_upload_of_file_should_create_columns_in_database(self):
        """Test for a table being created when csv is uploaded."""
        # Arrange
        file = self.create_file(
            self.table.name + ".csv", "name,city,age\nPhil,Aarhus,36"
        )

        # Act
        response = self.client.post(self.current_url, {"uploaded_file": file})

        # Assert
        self.assertEqual(file.name, self.table.original_file_name)
        self.assertRedirects(response, self.expected_redirect_url)
        self.assertEqual(3, self.table.columns_set.all().count(), "expects 3 columns")

    def test_extracted_column_names_formats(self):
        """Test for a table being created when csv is uploaded."""
        # Arrange
        file = self.create_file("file.csv", "DISPLAY_NAME,AGE\nPhil,36")

        # Act
        self.client.post(self.current_url, {"uploaded_file": file})

        # Assert
        column = Columns.objects.filter(extracted_name="DISPLAY_NAME").first()
        self.assertEqual("Display Name", column.display_name)
        self.assertEqual("display_name", column.machine_readable_name)

    def test_upload_failed_with_wrong_file_extension(self):
        """Test for error message when file is not ending on .csv."""
        file = self.create_file("file-with-wrong-ext.svg", "file content")

        response = self.client.post(self.current_url, {"uploaded_file": file})

        self.assertContains(response, "Unsupported file format: .svg")

    def test_upload_failed_with_no_rows_found(self):
        """Test for error if not able to extract headers from CSV."""
        file = self.create_file("file-with-bad-headers.csv", "name, age")

        response = self.client.post(self.current_url, {"uploaded_file": file})

        self.assertContains(response, "Invalid CSV. No rows found!")

    def test_resubmit_of_file_should_delete_prev_file_and_columns(self):
        """Resubmitting a file table should delete the previous file and columns."""
        # Arrange
        initial_file_content = "first_name,year\nHans,2000"
        expected_file_content = "name,city,age\nPhil,Aarhus,36"
        file1 = self.create_file("file.csv", initial_file_content)
        file2 = self.create_file("file.csv", expected_file_content)

        # Act
        self.client.post(self.current_url, {"uploaded_file": file1})
        self.client.post(self.current_url, {"uploaded_file": file2})

        # Assert
        files = Files.objects.all()
        columns = Columns.objects.all()
        self.assertEqual(1, files.count())
        self.assertEqual(3, columns.count())

        expected_columns = ["name", "city", "age"]
        actual_columns = list(map(lambda c: c.extracted_name, columns))
        self.assertEqual(actual_columns, expected_columns)

        actual_file_content = Path(files.first().server_file_path).read_text()
        self.assertEqual(expected_file_content, actual_file_content)

    def tearDown(self):
        """Called automatically by Django to clean up after test."""
        for file in Files.objects.all():
            file.delete()

    @staticmethod
    def create_file(name: str, content: str) -> io.BytesIO:
        """Create file for test."""
        file = io.BytesIO(content.encode("utf-8"))
        file.name = name
        return file

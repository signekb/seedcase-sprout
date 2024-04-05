"""Tests for the project id data view."""

import io

from django.test import TestCase
from django.urls import reverse

from sprout.models import ColumnMetadata, FileMetadata, TableMetadata
from sprout.tests.db_test_utils import create_table


class ProjectIdMetaDataTests(TestCase):
    """Tests for the file upload view."""

    def setUp(self):
        """Create a table and a column for testing."""
        self.table_metadata = TableMetadata.objects.create(
            name="Test Table",
            description="Test table description.",
        )
        self.column_metadata = ColumnMetadata.objects.create(
            table_metadata=self.table_metadata,
            extracted_name="TestColumn",
            machine_readable_name="test_column",
            display_name="Test Column",
            description="Test Description",
            data_type_id=0,
            allow_missing_value=True,
            allow_duplicate_value=True,
        )

        file = io.BytesIO(b"TestColumn,Letter\n1,A\n2,B\n3,C")
        file.name = "file-name.csv"
        self.file_metadata = FileMetadata.create_file_metadata(
            file, self.table_metadata.pk
        )

        self.url = reverse("metadata")
        self.empty_form = {}
        self.invalid_form = {"name": "Test/Table", "description": "Test description"}
        self.valid_form = {"name": "TestTable", "description": "Test description"}

    def test_view_renders(self):
        """Test that the get function renders."""
        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project-id-metadata-view.html")

    def test_view_shows_all_tables(self):
        """Test that the view shows all tables in TableMetadata."""
        # Arrange
        create_table("Table1").save()
        create_table("Table2").save()
        tables = TableMetadata.objects.all()

        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        for table in tables:
            self.assertContains(response, table.name)

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
        self.assertRedirects(
            response, "/metadata/create/2"
        )  # id is 2 because of the table created in the setUp method

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
        Tests that page isn't redirected when a valid form with a table name that
        already exists in the database is submitted.
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

"""Tests for the data import view."""

from django.test import TestCase
from django.urls import reverse

from sprout.models import TableMetadata


class DataImportTests(TestCase):
    """Tests for the data import view."""

    url = reverse("data-import")
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
        self.assertRedirects(response, "/metadata/create/1")

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

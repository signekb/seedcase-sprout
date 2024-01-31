from django.test import TestCase
from django.urls import reverse

from app.models import TableMetadata


class DataImportTests(TestCase):
    url = reverse("data_import")
    empty_form = {}
    invalid_form = {"name": "Test/Table", "description": "Test description"}
    valid_form = {"name": "TestTable", "description": "Test description"}

    def test_data_import_renders(self):
        """
        test_data_import_renders checks that tbe page is rendered using the expected
        template, when the response method is "GET"
        """

        # Arrange/Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "data-import.html")

    def test_fields_are_required(self):
        """
        test_fields_are_required checks that the expected errors occur when
        the form is empty (i.e., "This field is required)
        """
        # Arrange/Act
        response = self.client.post(self.url, self.empty_form)

        # Assert
        self.assertFormError(response, "form", "name", "This field is required.")
        self.assertFormError(response, "form", "description", "This field is required.")

    def test_redirect_with_valid_form(self):
        """
        test_redirect_with_valid_form checks that the page is redirected when a valid form
        is submitted
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
        """
        test_no_redirect_with_invalid_form_special_characters checks that the page
        isn't redirected when an invalid form with special characters in the "name" field
        is submitted
        """
        # Arrange/Act
        response = self.client.post(
            self.url,
            data=self.invalid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_with_valid_form_table_exists(self):
        """
        test_no_redirect_with_valid_form_table_exists checks that page isn't redirected
        when a valid form with a table name that already exists in the database is
        submitted
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

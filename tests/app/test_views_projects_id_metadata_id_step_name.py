from django.test import TestCase
from django.urls import reverse

from seedcase_sprout.app.models import Tables
from seedcase_sprout.app.views.projects_id_metadata_id.helpers import create_stepper_url
from tests.db_test_utils import create_table


class MetadataStepNameTests(TestCase):
    def setUp(self):
        self.current_url = reverse("projects-id-metadata-create")

        self.empty_form = {}
        self.invalid_form = {"name": "Test/Table", "description": "Test description"}
        self.valid_form = {"name": "TestTable", "description": "Test description"}

    def tests_redirect_on_valid_form(self):
        """Redirect to next step when form is valid."""
        # Arrange
        url = self.current_url

        # Act
        response = self.client.post(url, self.valid_form)

        # Assert
        table = Tables.objects.get(name=self.valid_form["name"])
        self.assertIsNotNone(table)
        self.assertRedirects(response, create_stepper_url(2, table.id))

    def test_no_redirect_if_form_is_empty(self):
        """No redirect when form is invalid because it is empty."""
        # Arrange
        url = self.current_url

        # Arrange/Act
        response = self.client.post(url, self.empty_form)

        # Assert
        # self.assertFormError(response, "form", "name", "This field is required.")
        # self.assertFormError(response, "form", "description",
        #   "This field is required.")
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_with_valid_form_table_exists(self):
        """Test that page isn't redirected when a table with the submitted name exists.
        Tests that page isn't redirected when a valid form with a table name that
        already exists in the database is submitted.
        """
        # Arrange
        Tables.objects.create(name="TestTable", description="Test description")

        # Act
        response = self.client.post(self.current_url, data=self.valid_form)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_no_redirect_with_invalid_form_special_characters(self):
        """Test that no redirection when the "name" field contains special characters.

        Tests that the page isn't redirected when an invalid form with special
        characters in the "name" field is submitted.
        """
        # Arrange/Act
        response = self.client.post(
            self.current_url,
            data=self.invalid_form,
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    def tests_name_edit_of_existing_table(self):
        """Edit name of existing table."""
        # Arrange
        table = create_table("InitialName")
        table.save()
        url = create_stepper_url(1, table_id=table.id)
        form_data = {"name": "NewTableName", "description": table.description}

        # Act
        response = self.client.post(url, form_data)

        # Assert
        table = Tables.objects.get(name=form_data["name"])
        self.assertRedirects(response, create_stepper_url(2, table.id))

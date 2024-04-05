"""Tests for forms."""

from django.test import TestCase

from sprout.forms import ColumnsForm
from sprout.models import DataTypes, TableMetadata


class ColumnsFormTest(TestCase):
    """Class of tests for the Metadata form."""

    def setUp(self):
        """Creating the data needed for the tests."""
        # Arrange: Create test instances for models
        self.table_metadata = TableMetadata.objects.create(name="TestTableKB")
        self.column_data_type = DataTypes.objects.create(
            display_name="TestStringFormat"
        )

    def test_form_invalid_when_no_data(self):
        """Test that a form created without data is invalid."""
        # Arrange: Create an instance of the form without providing any data
        form = ColumnsForm()

        # Act: Check if the form is not valid
        is_valid = form.is_valid()

        # Assert: Ensure the form is not valid
        self.assertFalse(is_valid)

    def test_form_valid_data(self):
        """Test that the validation works on correct data."""
        # Arrange: Create valid form data
        form_data = {
            "extracted_name": "TestName",
            "machine_readable_name": "test_name",
            "display_name": "TestDisplayName",
            "description": "This is the Description",
            "data_type": self.column_data_type.id,
            "allow_missing_value": True,
            "allow_duplicate_value": False,
        }

        # Act: Create an instance of the form with valid data
        form = ColumnsForm(data=form_data)
        is_valid = form.is_valid()

        # Assert: Ensure the form is valid
        self.assertTrue(is_valid)

    def test_form_invalid_data(self):
        """Test that the validation works on wrong data and throws an error."""
        # Arrange: Create invalid form data
        invalid_form_data = {
            "extracted_name": "",
            "machine_readable_name": "",
            "display_name": "",
            "description": "Description",
            "data_type": self.column_data_type.id,
            "allow_missing_value": True,
            "allow_duplicate_value": False,
        }

        # Act: Create an instance of the form with invalid data
        form = ColumnsForm(data=invalid_form_data)
        is_valid = form.is_valid()

        # Assert: Ensure the form is not valid
        self.assertFalse(is_valid)

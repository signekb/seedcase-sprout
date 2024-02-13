"""File for testing forms."""
from django.test import TestCase

from app.forms import TableMetadataForm
from app.models import TableMetadata


class TableMetadataFormTests(TestCase):
    """Class with tests for TableMetadataForm."""

    def test_table_name_contains_special_character(self):
        """Check for special characters.

        Checks that form validation fails when the table name includes a
        special character (here "/") (and description is provided).
        """
        # Arrange
        form_data = {"name": "Table/Name", "description": "Test description"}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"],
            [
                f"Please use only a-z, A-Z, 0-9, -, or _ when "
                f"specifying {list(form_data.keys())[0]}"
            ],
        )

    def test_table_name_contains_space(self):
        """test_table_name_contains_space Check for spaces in name.

        Checks that form validation fails when the table name includes a space
        (and description is provided)
        """
        # Arrange
        form_data = {"name": "Table Name", "description": "Test description"}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"],
            [
                f"Please use only a-z, A-Z, 0-9, -, or _ when "
                f"specifying {list(form_data.keys())[0]}"
            ],
        )

    def test_table_name_does_not_contain_special_characters(self):
        """Check for special characters.

        Checks that form validation succeeds when the table name doesn't
        include special characters (and description is provided)
        """
        # Arrange
        form_data = {
            "name": "TestTableName",
            "description": "Test description",
        }
        wrong_form_data = {
            "name": "Test(TableName",
            "description": "Test description",
        }

        # Act
        form = TableMetadataForm(data=form_data)
        wrong_form = TableMetadataForm(data=wrong_form_data)

        # Assert
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertFalse(wrong_form.is_valid())

    def test_table_name_exists_in_db(self):
        """Check if table already exists.

        Checks that form validation fails when a table with the provided name
        exists in the database (and description is provided)
        """
        # Arrange
        TableMetadata.objects.create(
            name="TestTable", description="Test description"
        )
        form_data = {"name": "TestTable", "description": "Test description"}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"],
            [
                "A table with this name already exists. "
                "Please provide another name."
            ],
        )

    def test_table_name_does_not_exist_in_db(self):
        """Checks that table doesn't exist already.

        Checks that form validation succeeds when the table name
        does not exist in the database (and description is provided)
        """
        # Arrange
        form_data = {
            "name": "TestTableName",
            "description": "Test description",
        }

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_table_name_empty(self):
        """Checks that form validation fails when table name is empty."""
        # Arrange
        form_data = {"name": ""}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_description_empty(self):
        """Check if description is empty.

        Checks that form validation fails when description is empty
        (and table name is provided).
        """
        # Arrange
        form_data = {"name": "TestTable", "description": ""}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["description"], ["This field is required."]
        )

    def test_description_not_empty(self):
        """Check if description isn't empty.

        Checks that form validation succeeds when description
        is not empty (and table name is provided)
        """
        # Arrange
        form_data = {"name": "TestTable", "description": "Test description"}

        # Act
        form = TableMetadataForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors.get("description"), None)

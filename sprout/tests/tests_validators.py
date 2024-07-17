"""Tests for validators."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from sprout.app.models import Tables
from sprout.app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class ValidateNoSpecialCharactersTests(TestCase):
    """Class with tests for validating the special characters validator."""

    def test_field_contains_special_character(self):
        """Test for field with special characters.

        Tests that validation fails with the expected message and code if the field
        contains a special character (here "ø").
        """
        # Arrange
        field_name = "name"
        field_value = "Søren"

        # Act
        with self.assertRaises(ValidationError) as context:
            validate_no_special_characters(
                field_name=field_name, field_value=field_value
            )

        # Assert
        self.assertEqual(
            context.exception.message,
            f"Please don't use spaces and only use upper or lower case letters "
            f"(a to z), numbers (0 to 9), -, or _ when specifying {field_name}",
        )
        self.assertEqual(context.exception.code, "invalid_value_special_characters")

    def test_field_contains_space(self):
        """Test for field with space.

        Tests that validation fails with the expected message and code if the field
        contains spaces.
        """
        # Arrange
        field_name = "name"
        field_value = "Jens Jensen"

        # Act
        with self.assertRaises(ValidationError) as context:
            validate_no_special_characters(
                field_name=field_name, field_value=field_value
            )

        # Assert
        self.assertEqual(
            context.exception.message,
            f"Please don't use spaces and only use upper or lower case letters "
            f"(a to z), numbers (0 to 9), -, or _ when specifying {field_name}",
        )
        self.assertEqual(context.exception.code, "invalid_value_special_characters")

    def test_field_does_not_contain_special_characters(self):
        """Test for field not containing special characters.

        Tests that validation doesn't fail if the field doesn't contain special
        characters.
        """
        # Arrange
        field_name = "name"
        field_value = "Kris"

        # Act
        try:
            val = validate_no_special_characters(
                field_name=field_name, field_value=field_value
            )
        except ValidationError as e:
            self.fail(f"Unexpected ValidationError: {e}")

        # Assert
        self.assertIsNone(val)


class ValidateTableNameDoesNotExistTests(TestCase):
    """Test for table does not exist validator."""

    def test_table_name_exists_in_db(self):
        """Test for a table name that already exists in database.

        Tests that validation fails with expected message and code if table_name already
        exists in the database.
        """
        # Arrange
        Tables.objects.create(name="TestTable", description="Test description")
        name = "TestTable"

        # Act
        with self.assertRaises(ValidationError) as context:
            validate_table_name_does_not_exist(name=name)
        # Assert
        self.assertEqual(
            context.exception.message,
            "A table with this name already exists. Please provide another name.",
        )
        self.assertEqual(context.exception.code, "invalid_table_name_already_exists")

    def test_table_name_does_not_exist_in_db(self):
        """Test for a table name that doesn't exist in the database.

        Tests that validation doesn't fail when ``table_name`` doesn't exist in the
        database.
        """
        # Arrange
        name = "TestTable"

        # Act
        try:
            value = validate_table_name_does_not_exist(name=name)
        except ValidationError as e:
            self.fail(f"Unexpected ValidationError: {e}")

        # Assert
        self.assertIsNone(value)

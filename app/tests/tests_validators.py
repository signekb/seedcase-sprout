from django.test import TestCase
from django.core.exceptions import ValidationError

from app.models import TableMetadata
from app.validators import (
    validate_no_special_characters,
    validate_table_name_does_not_exist,
)


class ValidateNoSpecialCharactersTests(TestCase):
    def test_field_contains_special_character(self):
        """
        test_field_contains_special_character checks that validation fails with the expected
        message and code if the field contains a special character (here "ø")
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
            f"Please use only a-z, A-Z, 0-9, -, or _ when specifying {field_name}",
        )
        self.assertEqual(context.exception.code, "invalid_value_special_characters")

    def test_field_contains_space(self):
        """
        test_field_contains_space checks that validation fails with the expected message and
        code if the field contains spaces
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
            f"Please use only a-z, A-Z, 0-9, -, or _ when specifying {field_name}",
        )
        self.assertEqual(context.exception.code, "invalid_value_special_characters")

    def test_field_does_not_contain_special_characters(self):
        """
        test_field_does_not_contain_special_characters checks that validation doesn't fail
        if the field doesn't include special characters
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
    def test_table_name_exists_in_db(self):
        """
        test_table_name_exists_in_db checks that validation fails with expected message
        and code if table_name already exists in the database.
        """
        # Arrange
        TableMetadata.objects.create(name="TestTable", description="Test description")
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
        """
        test_table_name_does_not_exist_in_db checks that validation doesn't fail
        when table_name doesn't exist in the database.
        """
        # Arrange
        name = "TestTable"

        # Act
        try:
            val = validate_table_name_does_not_exist(name=name)
        except ValidationError as e:
            self.fail(f"Unexpected ValidationError: {e}")

        # Assert
        self.assertIsNone(val)

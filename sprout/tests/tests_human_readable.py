from django.test import TestCase

from sprout.models.column_metadata import _convert_to_human_readable


class ConvertToHumanReadable(TestCase):
    """Tests to convert to human-readable format."""

    def test_snake_case_to_human_readable(self):
        string = "snake_case"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Snake Case", human_readable)

    def test_pascal_case_to_human_readable(self):
        string = "PascalCase"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Pascal Case", human_readable)

    def test_camel_case_to_human_readable(self):
        string = "camelCase"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Camel Case", human_readable)

    def test_lower_case_to_human_readable(self):
        string = "lower case"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Lower Case", human_readable)

    def test_upper_case_to_human_readable(self):
        string = "UPPER CASE"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Upper Case", human_readable)

    def test_upper_case_with_underscore_to_human_readable(self):
        string = "UPPER_CASE"

        human_readable = _convert_to_human_readable(string)

        self.assertEqual("Upper Case", human_readable)

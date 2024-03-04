from django.test import TestCase

from sprout.views.file_upload import _convert_to_snake_case


class ConvertToSnakeCase(TestCase):
    """Tests for the convert_to_snake_case utility function used in file upload"""

    def test_convert_to_snake_case_snake_case(self):
        string = _convert_to_snake_case("snake_case")

        self.assertEqual(string, "snake_case")

    def test_convert_to_snake_case_camel_case(self):
        string = _convert_to_snake_case("CamelCase")

        self.assertEqual(string, "camel_case")

    def test_convert_to_snake_case_kebab_case(self):
        string = _convert_to_snake_case("kebab-case")

        self.assertEqual(string, "kebab_case")

    def test_convert_to_snake_case_spaces_numbers_and_non_alphanumeric_characters(self):
        string = _convert_to_snake_case(" String with spaces  ")

        self.assertEqual(string, "string_with_spaces")

    def test_convert_to_snake_case_caps(self):
        string = _convert_to_snake_case("stringWithCAPSAndMORE")

        self.assertEqual(string, "string_with_caps_and_more")

    def test_convert_to_snake_case_numbers_and_non_alphanumeric_characters(self):
        string = _convert_to_snake_case("Num8ers & nona|phanumeric characters")

        self.assertEqual(string, "num8ers_nonaphanumeric_characters")

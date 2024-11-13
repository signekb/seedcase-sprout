from seedcase_sprout.core.utils import convert_to_snake_case


def test_convert_to_snake_case_snake_case():
    """Converts snake_case to a string in snake_case."""
    assert convert_to_snake_case("snake_case") == "snake_case"


def test_convert_to_snake_case_camel_case():
    """Converts camelCase to a string in snake_case."""
    assert convert_to_snake_case("CamelCase") == "camel_case"


def test_convert_to_snake_case_kebab_case():
    """Converts kebab-case to a string in snake_case."""
    assert convert_to_snake_case("kebab-case") == "kebab_case"


def test_convert_to_snake_case_spaces_numbers_and_non_alphanumeric_characters():
    """Converts a string with spaces, numbers, and non-alphanumeric characters to a
    string in snake_case."""
    assert convert_to_snake_case(" String with spaces  ") == "string_with_spaces"


def test_convert_to_snake_case_caps():
    """Converts a string with capital letters to a string in snake_case."""
    assert convert_to_snake_case("stringWithCAPSAndMORE") == "string_with_caps_and_more"


def test_convert_to_snake_case_numbers_and_non_alphanumeric_characters():
    """Converts a string with numbers and non-alphanumeric characters to a string in
    snake_case."""
    assert (
        convert_to_snake_case("Num8ers & nona|phanumeric characters")
        == "num8ers_nonaphanumeric_characters"
    )

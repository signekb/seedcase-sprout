from seedcase_sprout.core.utils import convert_to_human_readable


def test_snake_case_to_human_readable():
    """Converts snake_case to a human readable string in title case."""
    assert convert_to_human_readable("snake_case") == "Snake Case"


def test_pascal_case_to_human_readable():
    """Converts PascalCase to human readable title case"""
    assert convert_to_human_readable("PascalCase") == "Pascal Case"


def test_camel_case_to_human_readable():
    """Converts camelCase to a human readable string in title case."""
    assert convert_to_human_readable("camelCase") == "Camel Case"


def test_lower_case_to_human_readable():
    """Converts lower case to a human readable string in title case."""
    assert convert_to_human_readable("lower case") == "Lower Case"


def test_upper_case_to_human_readable():
    """Converts UPPER CASE to a human readable string in title case."""
    assert convert_to_human_readable("UPPER CASE") == "Upper Case"


def test_upper_case_with_underscore_to_human_readable():
    """Converts UPPER_CASE to a human readable string in title case."""
    assert convert_to_human_readable("UPPER_CASE") == "Upper Case"

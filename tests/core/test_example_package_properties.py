from seedcase_sprout.core.example_package_properties import example_package_properties
from seedcase_sprout.core.sprout_checks.check_package_properties import (
    check_package_properties,
)


def test_creates_correct_properties_object():
    assert check_package_properties(example_package_properties())

from seedcase_sprout.core.examples import (
    example_package_properties,
    example_resource_properties,
)
from seedcase_sprout.core.sprout_checks.check_package_properties import (
    check_package_properties,
)
from seedcase_sprout.core.sprout_checks.check_resource_properties import (
    check_resource_properties,
)


def test_creates_correct_package_properties_object():
    assert check_package_properties(example_package_properties())


def test_creates_correct_resource_properties_object():
    assert check_resource_properties(example_resource_properties())

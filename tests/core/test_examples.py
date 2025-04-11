from seedcase_sprout.core.examples import (
    example_package_properties,
    example_resource_properties,
    example_resource_properties_all_types,
)
from seedcase_sprout.core.sprout_checks.check_properties import (
    check_package_properties,
    check_resource_properties,
)


def test_creates_correct_package_properties_object():
    assert check_package_properties(example_package_properties())


def test_creates_correct_resource_properties_object():
    assert check_resource_properties(example_resource_properties())


def test_creates_correct_resource_properties_object_all_types():
    assert check_resource_properties(example_resource_properties_all_types())


def xtest_example_data_matches_resource_properties():
    # TODO: Update when `check_data()` has been finished
    # data = example_data()
    # assert check_data(data, example_resource_properties()) is data
    ...


def xtest_example_data_matches_resource_properties_all_types():
    # TODO: Update when `check_data()` has been finished
    # data = example_data_all_types()
    # assert check_data(data, example_resource_properties_all_types()) is data
    ...

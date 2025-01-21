from pytest import fixture, mark

from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.sprout_checks.get_blank_value_for_type import (
    get_blank_value_for_type,
)
from seedcase_sprout.core.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)
from seedcase_sprout.core.sprout_checks.required_fields import (
    PACKAGE_SPROUT_REQUIRED_FIELDS,
)


@fixture
def properties():
    return PackageProperties(
        name="package-1",
        id="abc1",
        title="Package 1",
        description="A package.",
        version="1.0.0",
        created="2024-05-14T05:00:01+00:00",
        licenses=[{"name": "a-license"}],
        contributors=[{"title": "a contributor"}],
        sources=[{"title": "a source"}],
    ).compact_dict


# Check required fields


def test_passes_full_package_properties(properties):
    """Should pass with a full set of package properties."""
    assert get_sprout_package_errors(properties, check_required=True) == []


@mark.parametrize("name,type", PACKAGE_SPROUT_REQUIRED_FIELDS.items())
def test_error_found_if_fields_are_blank(properties, name, type):
    """Should find an error if there is one required field that is present but blank."""
    properties[name] = get_blank_value_for_type(type)

    errors = get_sprout_package_errors(properties, check_required=True)

    assert len(errors) == 1
    assert errors[0].json_path == f"$.{name}"
    assert errors[0].validator == "blank"


@mark.parametrize("name", PACKAGE_SPROUT_REQUIRED_FIELDS.keys())
def test_error_found_if_required_fields_are_missing(properties, name):
    """Should find an error if there is a missing required field and required fields are
    enforced."""
    del properties[name]

    errors = get_sprout_package_errors(properties, check_required=True)

    assert len(errors) == 1
    assert errors[0].json_path == f"$.{name}"
    assert errors[0].validator == "required"


# Do not check required fields


def test_passes_full_package_properties_without_required_check(properties):
    """Should pass with a full set of package properties."""
    assert get_sprout_package_errors(properties, check_required=False) == []


def test_passes_partial_package_properties_without_required_check():
    """Should pass with missing required fields when required fields are not
    enforced."""
    assert get_sprout_package_errors({}, check_required=False) == []


@mark.parametrize("name,type", PACKAGE_SPROUT_REQUIRED_FIELDS.items())
def test_error_found_if_fields_are_blank_without_required_check(properties, name, type):
    """Should find an error if there is one required field that is present but blank."""
    properties[name] = get_blank_value_for_type(type)

    errors = get_sprout_package_errors(properties, check_required=False)

    assert len(errors) == 1
    assert errors[0].json_path == f"$.{name}"
    assert errors[0].validator == "blank"

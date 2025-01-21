from pytest import fixture, mark, raises

from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.sprout_checks.check_package_properties import (
    check_package_properties,
)
from seedcase_sprout.core.sprout_checks.get_blank_value_for_type import (
    get_blank_value_for_type,
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


@mark.parametrize("check_required", [True, False])
def test_passes_full_package_properties(properties, check_required):
    """Should pass if all required fields are present and correct."""
    assert (
        check_package_properties(properties, check_required=check_required)
        == properties
    )


@mark.parametrize("check_required", [True, False])
@mark.parametrize("resources", [[], [{}], [{"name": "name", "path": "data.csv"}]])
def test_passes_without_checking_resources(resources, properties, check_required):
    """Should pass well-formed package properties without checking individual resource
    ``
        properties."""
    properties["resources"] = resources

    assert (
        check_package_properties(properties, check_required=check_required)
        == properties
    )


@mark.parametrize("check_required", [True, False])
def test_raises_error_for_resources_of_wrong_type(properties, check_required):
    """Should raise an error if there is a `resources` field with a value of the wrong
    type."""
    properties["resources"] = 123

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=check_required)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].validator == "type"
    assert errors[0].json_path == "$.resources"


@mark.parametrize("field", PACKAGE_SPROUT_REQUIRED_FIELDS.keys())
def test_raises_error_if_required_field_is_missing(properties, field):
    """Should raise an error if a required field is missing."""
    del properties[field]

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=True)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == f"$.{field}"
    assert errors[0].validator == "required"


def test_raises_error_if_nested_required_fields_are_missing():
    """Should raise errors if nested required fields are missing."""
    properties = PackageProperties(
        name="package-1",
        id="abc1",
        title="Package 1",
        description="A package.",
        version="1.0.0",
        created="2024-05-14T05:00:01+00:00",
        licenses=[{}],
        contributors=[{}],
        sources=[{}],
    ).compact_dict

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=True)

    required_errors = [
        error for error in error_info.value.exceptions if error.validator == "required"
    ]
    assert [error.json_path for error in required_errors] == [
        "$.contributors[0].title",
        "$.licenses[0].name",
        "$.licenses[0].path",
        "$.sources[0].title",
    ]


@mark.parametrize("check_required", [True, False])
def test_raises_error_for_mismatched_pattern(properties, check_required):
    """Should raise an error if `name` violates the pattern."""
    properties["name"] = "a name with spaces"

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=check_required)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "pattern"


@mark.parametrize("check_required", [True, False])
def test_raises_error_for_mismatched_format(properties, check_required):
    """Should raise an error if `homepage` violates the format."""
    properties["homepage"] = "not a URL"

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=check_required)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.homepage"
    assert errors[0].validator == "format"


@mark.parametrize("check_required", [True, False])
@mark.parametrize("name,type", PACKAGE_SPROUT_REQUIRED_FIELDS.items())
def test_raises_error_if_fields_are_blank(properties, name, type, check_required):
    """Should raise an error if there is one required field that is present but
    blank."""
    properties[name] = get_blank_value_for_type(type)

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=check_required)

    blank_errors = [
        error for error in error_info.value.exceptions if error.validator == "blank"
    ]

    assert len(blank_errors) == 1
    assert blank_errors[0].json_path == f"$.{name}"


@mark.parametrize("check_required", [True, False])
def test_raises_error_if_nested_fields_are_blank(check_required):
    """Should raise errors if required nested fields are present but blank."""
    properties = PackageProperties(
        name="package-1",
        id="abc1",
        title="Package 1",
        description="A package.",
        version="1.0.0",
        created="2024-05-14T05:00:01+00:00",
        licenses=[{"name": "", "path": ""}],
        contributors=[{"title": ""}],
        sources=[{"title": ""}],
    ).compact_dict

    with raises(ExceptionGroup) as error_info:
        check_package_properties(properties, check_required=check_required)

    blank_errors = [
        error for error in error_info.value.exceptions if error.validator == "blank"
    ]
    assert [error.json_path for error in blank_errors] == [
        "$.contributors[0].title",
        "$.licenses[0].name",
        "$.licenses[0].path",
        "$.sources[0].title",
    ]


def test_passes_partial_package_properties_without_required_check():
    """Should pass properties with missing required fields when these are not
    enforced."""
    assert check_package_properties({}, check_required=False) == {}

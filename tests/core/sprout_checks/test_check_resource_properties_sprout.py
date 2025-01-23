from pathlib import Path

from pytest import fixture, mark, raises

from seedcase_sprout.core.checks.check_error import CheckError
from seedcase_sprout.core.checks.check_error_matcher import CheckErrorMatcher
from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.sprout_checks.check_resource_properties import (
    check_resource_properties,
)
from seedcase_sprout.core.sprout_checks.get_blank_value_for_type import (
    get_blank_value_for_type,
)
from seedcase_sprout.core.sprout_checks.required_fields import (
    RESOURCE_SPROUT_REQUIRED_FIELDS,
)


@fixture
def properties():
    return ResourceProperties(
        name="resource-1",
        path=str(Path("resources", "1", "data.parquet")),
        title="Resource 1",
        description="A resource.",
    ).compact_dict


def test_passes_full_resource_properties(properties):
    """Should pass if all required fields are present and correct."""
    assert check_resource_properties(properties) == properties


@mark.parametrize(
    "field",
    RESOURCE_SPROUT_REQUIRED_FIELDS.keys(),
)
def test_error_raised_if_required_field_is_missing(properties, field):
    """Should raise an error if a required field is missing."""
    del properties[field]

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == f"$.{field}"
    assert errors[0].validator == "required"


@mark.parametrize("path", ["", [], str(Path("resources", "1")), "/bad/path/data.csv"])
def test_error_raised_if_data_path_is_incorrect_(properties, path):
    """Should raise an error if `path` contains no resource ID, is not a string, or is
    otherwise malformed."""
    properties["path"] = path

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) >= 1
    assert all(
        isinstance(error, CheckError) and error.json_path.endswith("path")
        for error in errors
    )


def test_error_raised_if_inline_data_is_set(properties):
    """Should raise an error if inline data is set."""
    properties["data"] = "some data"

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == "$.data"
    assert errors[0].validator == "inline-data"


@mark.parametrize("name,type", RESOURCE_SPROUT_REQUIRED_FIELDS.items())
def test_error_raised_if_fields_are_blank(properties, name, type):
    """Should raise an error if there is one required field that is present but
    blank."""
    properties[name] = get_blank_value_for_type(type)

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    blank_errors = [
        error for error in error_info.value.exceptions if error.validator == "blank"
    ]

    assert len(blank_errors) == 1
    assert isinstance(blank_errors[0], CheckError)
    assert blank_errors[0].json_path == f"$.{name}"


def test_error_raised_for_mismatched_pattern(properties):
    """Should raise an error if `name` violates the pattern."""
    properties["name"] = "a name with spaces"

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "pattern"


def test_error_raised_for_mismatched_format(properties):
    """Should raise an error if `homepage` violates the format."""
    properties["homepage"] = "not a URL"

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == "$.homepage"
    assert errors[0].validator == "format"


def test_error_raised_for_mismatched_type(properties):
    """Should raise an error if `name` violates the type constraint."""
    properties["name"] = 123

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "type"


def test_error_raised_for_only_sprout_specific_errors(properties):
    """Errors should be triggered by only those Data Package standard violations that
    are relevant for Sprout."""
    properties["path"] = 123

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(properties)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert isinstance(errors[0], CheckError)
    assert errors[0].json_path == "$.path"
    assert errors[0].validator == "type"


def test_ignored_errors_should_not_make_check_fail():
    """Check should not fail if triggered by an error that is ignored."""
    assert (
        check_resource_properties({}, ignore=[CheckErrorMatcher(validator="required")])
        == {}
    )


def test_excludes_ignored_errors_from_output(properties):
    """Errors that are ignored should not be in error output."""
    properties["name"] = "invalid name with spaces"
    properties["path"] = 123

    with raises(ExceptionGroup) as error_info:
        check_resource_properties(
            properties, ignore=[CheckErrorMatcher(json_path="path")]
        )

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "pattern"

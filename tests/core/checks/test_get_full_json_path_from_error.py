from jsonschema import ValidationError
from pytest import mark

from seedcase_sprout.core.checks.get_full_json_path_from_error import (
    get_full_json_path_from_error,
)

required_error = ValidationError(
    message="'name' is a required property", path=[], validator="required"
)

type_error = ValidationError(
    message="Some other validation error",
    path=["data", "attributes", "name"],
    validator="type",
)

malformed_required_error = ValidationError(
    message="Property 'x' is missing, but no required property message",
    path=["data"],
    validator="required",
)

array_path_error = ValidationError(
    message="'name' is a required property",
    path=["data", "items", 0],
    validator="required",
)


@mark.parametrize("error", [required_error, array_path_error])
def test_returns_correct_path_for_required_error(error):
    """Should return the correct json_path for a 'required' error."""
    json_path = error.json_path + ".name"
    assert get_full_json_path_from_error(error) == json_path


def test_does_not_modify_path_for_other_error():
    """Should not modify the path for an error that is not a 'required' error."""
    json_path = type_error.json_path
    assert get_full_json_path_from_error(type_error) == json_path


def test_does_not_modify_path_for_required_error_with_malformed_message():
    """Should not modify the path for a 'required' error if the error has a malformed /
    unexpected message."""
    json_path = malformed_required_error.json_path
    assert get_full_json_path_from_error(malformed_required_error) == json_path


def test_does_not_mutate_original_error():
    """Should not change the original error object."""
    get_full_json_path_from_error(required_error)

    assert required_error.json_path == "$"

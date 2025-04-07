from jsonschema import ValidationError
from pytest import mark

from seedcase_sprout.core.check_datapackage.unwrap_errors import unwrap_errors

simple_error = ValidationError(message="Simple error", path=["field1"], validator="val")

nested_error = ValidationError(
    message="Nested error", path=["field2"], validator="val", context=[simple_error]
)

deeply_nested_error = ValidationError(
    message="Deeply nested error",
    path=["field3"],
    validator="val",
    context=[nested_error, simple_error],
)


@mark.parametrize(
    "errors",
    [
        ([]),
        ([simple_error]),
        ([simple_error] * 8),
    ],
)
def test_unwraps_flat_errors(errors):
    """Should unwrap a flat list of errors."""
    assert unwrap_errors(errors) == errors


def test_unwraps_nested_errors():
    """Should unwrap a nested list of errors."""
    assert unwrap_errors([nested_error]) == [nested_error, simple_error]


def test_unwraps_deeply_nested_errors():
    """Should unwrap a deeply nested list of errors."""
    assert unwrap_errors([deeply_nested_error]) == [
        deeply_nested_error,
        nested_error,
        simple_error,
        simple_error,
    ]


def test_unwraps_multiple_toplevel_errors():
    """Should unwrap a list of errors with multiple top-level errors."""
    assert unwrap_errors([simple_error, nested_error]) == [
        simple_error,
        nested_error,
        simple_error,
    ]

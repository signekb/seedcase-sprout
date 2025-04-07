from jsonschema import ValidationError
from pytest import mark

from seedcase_sprout.core.check_datapackage.check_error import CheckError
from seedcase_sprout.core.check_datapackage.validation_errors_to_check_errors import (
    COMPLEX_VALIDATORS,
    validation_errors_to_check_errors,
)

simple_error = ValidationError(
    message="123 is not of type 'string'", path=["name"], validator="type"
)

nested_error = ValidationError(
    message="{} is not valid under any of the given schemas",
    path=["items", 0],
    validator="oneOf",
    context=[
        ValidationError(
            message="'name' is a required property",
            path=[],
            validator="required",
        ),
        ValidationError(
            message="'title' is a required property",
            path=[],
            validator="required",
        ),
    ],
)

deeply_nested_error = ValidationError(
    message="Top-level error",
    path=["user"],
    validator="a-validator",
    context=[
        ValidationError(
            message="Mid-level error",
            path=["address"],
            validator="b-validator",
            context=[
                ValidationError(
                    message="Low-level error", path=["street"], validator="c-validator"
                )
            ],
        )
    ],
)


def test_processes_flat_errors():
    """Should unwrap and transform a flat list of errors into `CheckError`s."""
    errors = iter([simple_error])

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message=simple_error.message,
            json_path=simple_error.json_path,
            validator=simple_error.validator,
        )
    ]


def test_processes_nested_errors():
    """Should flatten nested errors into a single list of `CheckError`s."""
    errors = iter([nested_error])

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message=nested_error.context[0].message,
            json_path="$.items[0].name",
            validator=nested_error.context[0].validator,
        ),
        CheckError(
            message=nested_error.context[1].message,
            json_path="$.items[0].title",
            validator=nested_error.context[1].validator,
        ),
    ]


def test_processes_deeply_nested_errors():
    """Should unwrap deeply nested errors and transform them into `CheckError`s."""
    errors = iter([deeply_nested_error])

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message="Top-level error",
            json_path="$.user",
            validator="a-validator",
        ),
        CheckError(
            message="Mid-level error",
            json_path="$.user.address",
            validator="b-validator",
        ),
        CheckError(
            message="Low-level error",
            json_path="$.user.address.street",
            validator="c-validator",
        ),
    ]


def test_processes_multiple_toplevel_errors():
    """Should transform a complex error list with multiple top-level and nested errors
    into `CheckError`s."""
    errors = iter(
        [simple_error, deeply_nested_error, simple_error, nested_error, simple_error]
    )

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message=nested_error.context[0].message,
            json_path="$.items[0].name",
            validator=nested_error.context[0].validator,
        ),
        CheckError(
            message=nested_error.context[1].message,
            json_path="$.items[0].title",
            validator=nested_error.context[1].validator,
        ),
        CheckError(
            message=simple_error.message,
            json_path="$.name",
            validator=simple_error.validator,
        ),
        CheckError(
            message="Top-level error",
            json_path="$.user",
            validator="a-validator",
        ),
        CheckError(
            message="Mid-level error",
            json_path="$.user.address",
            validator="b-validator",
        ),
        CheckError(
            message="Low-level error",
            json_path="$.user.address.street",
            validator="c-validator",
        ),
    ]


@mark.parametrize("validator", COMPLEX_VALIDATORS)
def test_ignores_complex_validators(validator):
    """Should ignore errors from validators in the COMPLEX_VALIDATORS set."""
    errors = iter(
        [
            ValidationError(
                message="{} is not valid under any of the given schemas",
                path=["items", 0],
                validator=validator,
            )
        ]
    )

    assert validation_errors_to_check_errors(errors) == []


def test_removes_duplicate_errors():
    """Should remove duplicate `CheckError`s after transformation."""
    errors = iter([simple_error] * 8)

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message=simple_error.message,
            json_path=simple_error.json_path,
            validator=simple_error.validator,
        )
    ]


def test_sorts_errors_by_json_path():
    """Should sort errors by `json_path`."""
    errors = iter(
        [
            ValidationError(
                message="First error", path=["data", "b"], validator="type"
            ),
            ValidationError(
                message="Second error", path=["data", "a"], validator="type"
            ),
            ValidationError(
                message="Third error", path=["data", "c"], validator="type"
            ),
        ]
    )

    assert validation_errors_to_check_errors(errors) == [
        CheckError(message="Second error", json_path="$.data.a", validator="type"),
        CheckError(message="First error", json_path="$.data.b", validator="type"),
        CheckError(message="Third error", json_path="$.data.c", validator="type"),
    ]


def test_adds_field_name_for_required_errors():
    """Should add field name for errors triggered by the 'required' validator."""
    errors = iter(
        [
            ValidationError(
                message="'name' is a required property", path=[], validator="required"
            )
        ]
    )

    assert validation_errors_to_check_errors(errors) == [
        CheckError(
            message="'name' is a required property",
            json_path="$.name",
            validator="required",
        )
    ]

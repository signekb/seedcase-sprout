from pytest import mark

from seedcase_sprout.core.properties import FieldProperties
from seedcase_sprout.core.sprout_checks.get_pandera_checks import (
    get_pandera_checks,
)


@mark.parametrize(
    "field_type",
    [
        "boolean",
        "time",
        "datetime",
        "date",
        "year",
        "yearmonth",
        "duration",
        "object",
        "array",
        "geopoint",
    ],
)
def test_returns_check_for_field_type(field_type):
    """Should return at least 1 check for the listed field types."""
    assert get_pandera_checks(FieldProperties(type=field_type))


@mark.parametrize("format", ["email", "binary", "uuid"])
def test_returns_check_for_string_format(format):
    """Should return at least 1 check for the listed string formats."""
    field = FieldProperties(type="string", format=format)

    assert get_pandera_checks(field)


@mark.parametrize("format", ["default", None])
def test_returns_no_checks_when_string_format_is_default(format):
    """Should return no checks for string fields with the default format."""
    field = FieldProperties(type="string", format=format)

    assert get_pandera_checks(field) == []


@mark.parametrize("field_type", ["any", None, "unknown"])
def test_returns_no_checks_when_field_type_any_or_unknown(field_type):
    """Should return no checks for fields whose type is unknown, any, or the default."""
    assert get_pandera_checks(FieldProperties(type=field_type)) == []

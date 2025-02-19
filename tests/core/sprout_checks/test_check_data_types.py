from pytest import mark
from xmlschema.names import (
    XSD_BASE64_BINARY,
    XSD_DATE,
    XSD_DATETIME,
    XSD_DURATION,
    XSD_GYEAR,
    XSD_GYEAR_MONTH,
    XSD_TIME,
)

from seedcase_sprout.core.sprout_checks.check_data_types import (
    check_is_email,
    check_is_geopoint,
    check_is_json,
    check_is_uuid,
    check_is_xml_type,
)


@mark.parametrize(
    "value,xml_type,expected",
    [
        ("2002-10-10T12:00:00.34-05:00", XSD_DATETIME, True),
        ("2002-10-10T17:00:00X", XSD_DATETIME, False),
        ("2002-10-10", XSD_DATE, True),
        ("99", XSD_DATE, False),
        ("15:00:59", XSD_TIME, True),
        ("2002-10-10T12:00:00", XSD_TIME, False),
        ("2014", XSD_GYEAR, True),
        ("99", XSD_GYEAR, False),
        ("2014-12", XSD_GYEAR_MONTH, True),
        ("2014-13", XSD_GYEAR_MONTH, False),
        ("P1Y2M3DT10H30M45.343S", XSD_DURATION, True),
        ("0Y1347M0D", XSD_DURATION, False),
        ("c29tZSB0ZXh0IDEyMw==", XSD_BASE64_BINARY, True),
        ("some text 123", XSD_BASE64_BINARY, False),
        ("2022", "unknown_type", False),
    ],
)
def test_checks_xml_type(value, xml_type, expected):
    """Should determine if values is a XML data types."""
    assert check_is_xml_type(value, xml_type) is expected


@mark.parametrize(
    "json_object,expected",
    [
        ("{}", True),
        (
            (
                '{"outer": "value", "inner": {"prop1": 123, '
                '"prop2": [1, 2, null], "prop3": true}}'
            ),
            True,
        ),
        ("[]", False),
        ("not,json,,", False),
        ('"[{"prop1": "value"}, {"prop2": 123}]"', False),
    ],
)
def test_checks_json_object(json_object, expected):
    """Should determine if the input is a JSON object."""
    assert check_is_json(json_object, dict) is expected


@mark.parametrize(
    "json_array,expected",
    [
        ("[]", True),
        ('[{"prop1": "value"}, {"prop2": 123}]', True),
        ("{}", False),
        ("not,json,,", False),
        ('{"name": "value"}', False),
    ],
)
def test_checks_json_array(json_array, expected):
    """Should determine if the input is a JSON array."""
    assert check_is_json(json_array, list) is expected


@mark.parametrize(
    "geopoint,expected",
    [
        ("90, 180", True),
        ("-90, -180", True),
        ("0, 0", True),
        ("5, 45", True),
        ("5.9999, 45.0000", True),
        ("5,45", True),
        ("5 , 45", True),
        ("5 45", False),
        ("45", False),
        ("", False),
        ("180, 90", False),
        ("91, 181", False),
        ("-91, -181", False),
        ("A, B", False),
    ],
)
def test_checks_geopoint(geopoint, expected):
    """Should determine if the input is a geopoint."""
    assert check_is_geopoint(geopoint) is expected


@mark.parametrize(
    "email,expected",
    [
        ("j_ane.d-oe99@email.co.uk", True),
        ("@", False),
        ("@email.co.uk", False),
        ("jane@@email.co.uk", False),
        ("jane@", False),
        ("jane@email", False),
        ("jane@email.", False),
        (f"jane.doe{'x' * 256}@email.co.uk", False),
    ],
)
def test_checks_email(email, expected):
    """Should determine if the input is (likely to be) an email address."""
    assert check_is_email(email) is expected


@mark.parametrize(
    "uuid,expected",
    [
        ("8c085e68-a36f-4cf7-9341-cdf2b1792657", True),
        ("some text", False),
        ("1234", False),
    ],
)
def test_checks_uuid(uuid, expected):
    """Should determine if the input can be parsed as a UUID."""
    assert check_is_uuid(uuid) is expected

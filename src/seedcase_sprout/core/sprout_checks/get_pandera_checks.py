import pandera.polars as pa
from xmlschema.names import (
    XSD_BASE64_BINARY,
    XSD_DATE,
    XSD_DATETIME,
    XSD_DURATION,
    XSD_GYEAR,
    XSD_GYEAR_MONTH,
    XSD_TIME,
)

from seedcase_sprout.core.properties import FieldProperties
from seedcase_sprout.core.sprout_checks.check_data_types import (
    check_is_email,
    check_is_geopoint,
    check_is_json,
    check_is_uuid,
    check_is_xml_type,
)

# https://datapackage.org/standard/table-schema/#boolean
BOOLEAN_VALUES = {"false", "False", "FALSE", "0", "true", "True", "TRUE", "1"}

STRING_FORMAT_CHECKS = {
    "email": pa.Check(
        check_is_email,
        element_wise=True,
        error="The given value doesn't seem to be a correctly formatted email address.",
    ),
    "binary": pa.Check(
        lambda value: check_is_xml_type(value, XSD_BASE64_BINARY),
        element_wise=True,
        error=(
            "The given value doesn't seem to be formatted correctly as binary data. "
            "Binary data is expected to be Base64-encoded."
        ),
    ),
    "uuid": pa.Check(
        check_is_uuid,
        element_wise=True,
        error="The given value doesn't seem to be a correctly formatted UUID.",
    ),
}


def get_pandera_checks(field: FieldProperties) -> list[pa.Check]:
    """Returns the Pandera checks appropriate for the field's format and data type.

    Args:
        field: The field to get the checks for.

    Returns:
        The appropriate Pandera checks.
    """
    if field.type == "string" and (
        format_check := STRING_FORMAT_CHECKS.get(field.format, None)
    ):
        return [format_check]

    match field.type:
        case "boolean":
            return [
                pa.Check(
                    lambda value: value in BOOLEAN_VALUES,
                    element_wise=True,
                    error=f"The given value needs to be one of {BOOLEAN_VALUES}.",
                )
            ]

        case "time":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_TIME),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "time value. The expected format for time values is HH:MM:SS. "
                        "See https://www.w3.org/TR/xmlschema-2/#time for more "
                        "information."
                    ),
                )
            ]

        case "datetime":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_DATETIME),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "datetime value. The expected format for datetime values is "
                        "YYYY-MM-DDTHH:MM:SS with optional milliseconds and time zone "
                        "information. See https://www.w3.org/TR/xmlschema-2/#dateTime "
                        "for more information."
                    ),
                )
            ]

        case "date":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_DATE),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "date value. The expected format for date values is YYYY-MM-DD."
                        " See https://www.w3.org/TR/xmlschema-2/#date for more "
                        "information."
                    ),
                )
            ]

        case "year":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_GYEAR),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "year value. The expected format for year values is YYYY. "
                        "See https://www.w3.org/TR/xmlschema-2/#gYear for more "
                        "information."
                    ),
                )
            ]

        case "yearmonth":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_GYEAR_MONTH),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "yearmonth value. The expected format for yearmonth values is "
                        "YYYY-MM. See https://www.w3.org/TR/xmlschema-2/#gYearMonth "
                        "for more information."
                    ),
                )
            ]

        case "duration":
            return [
                pa.Check(
                    lambda value: check_is_xml_type(value, XSD_DURATION),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "duration value. The expected format for duration values is "
                        "PnYnMnDTnHnMnS. See https://www.w3.org/TR/xmlschema-2/#duration"
                        " for more information."
                    ),
                )
            ]

        case "object":
            return [
                pa.Check(
                    lambda value: check_is_json(value, dict),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "JSON object."
                    ),
                )
            ]

        case "array":
            return [
                pa.Check(
                    lambda value: check_is_json(value, list),
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "JSON array."
                    ),
                )
            ]

        case "geopoint":
            return [
                pa.Check(
                    check_is_geopoint,
                    element_wise=True,
                    error=(
                        "The given value doesn't seem to be a correctly formatted "
                        "geographical point. The expected format for geographical "
                        "points is LAT, LONG."
                    ),
                )
            ]

        case _:
            return []

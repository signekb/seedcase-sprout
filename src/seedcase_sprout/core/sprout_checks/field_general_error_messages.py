from seedcase_sprout.core.properties import FieldType
from seedcase_sprout.core.sprout_checks.check_column_data_types import BOOLEAN_VALUES

DATA_TYPES_URL = "https://sprout.seedcase-project.org/docs/design/interface/data-types#"

FIELD_GENERAL_ERROR_MESSAGES: dict[FieldType, str] = {
    "boolean": f"The given value needs to be one of {BOOLEAN_VALUES}.",
    "year": (
        "The given value doesn't seem to be a correctly formatted year value. "
        "The expected format for year values is YYYY. See "
        f"{DATA_TYPES_URL}year for more information."
    ),
    "datetime": (
        "The given value doesn't seem to be a correctly formatted datetime value. "
        "The expected format for datetime values is YYYY-MM-DDTHH:MM:SS with optional "
        f"milliseconds and time zone information. See {DATA_TYPES_URL}datetime "
        "for more information."
    ),
    "date": (
        "The given value doesn't seem to be a correctly formatted date value. "
        "The expected format for date values is YYYY-MM-DD. See "
        f"{DATA_TYPES_URL}date for more information."
    ),
    "time": (
        "The given value doesn't seem to be a correctly formatted time value. "
        "The expected format for time values is HH:MM:SS. See "
        f"{DATA_TYPES_URL}time for more information."
    ),
    "yearmonth": (
        "The given value doesn't seem to be a correctly formatted yearmonth value. "
        "The expected format for yearmonth values is YYYY-MM. See "
        f"{DATA_TYPES_URL}yearmonth for more information."
    ),
    "geopoint": (
        "The given value doesn't seem to be a correctly formatted geographical point. "
        "The expected format for geographical points is LAT, LONG. See "
        f"{DATA_TYPES_URL}geopoint for more information."
    ),
    "duration": (
        "The given value doesn't seem to be a correctly formatted duration value. "
        "The expected format for duration values is PnYnMnDTnHnMnS. See "
        f"{DATA_TYPES_URL}duration for more information."
    ),
    "object": "The given value doesn't seem to be a correctly formatted JSON object.",
    "array": "The given value doesn't seem to be a correctly formatted JSON array.",
    "geojson": "The given value doesn't seem to be a correctly formatted JSON object.",
}

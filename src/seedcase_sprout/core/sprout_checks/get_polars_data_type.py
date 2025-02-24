import polars as pl

from seedcase_sprout.core.properties import FieldType


def get_polars_data_type(field_type: FieldType | None) -> pl.DataType:
    """Maps Frictionless field types to Polars data types.

    If the Frictionless field type has formatting constraints that are not included
    in any specialised Polars data type, the mapping is to string. The formatting
    constraints are then checked without Polars.

    Args:
        field_type: The Frictionless field type to map.

    Returns:
        The Polars data type the field is mapped to.

    Raises:
        NotImplementedError: If Sprout doesn't yet support the Frictionless field type.
    """
    match field_type:
        case "geojson":
            raise NotImplementedError()
        # While Polars does have most of these data types, there isn't a
        # perfect overlap between them and what Frictionless has, even
        # if they have similar/same names for the types. For example,
        # checks against date/datetimes/times types are different between
        # Polars and Frictionless. Or the way booleans get treated. Polars
        # may cast `123` to True, but Frictionless will indicate it is not
        # a boolean. We'll slowly improve on this as we use Sprout.
        case (
            "string"
            | "boolean"
            | "datetime"
            | "date"
            | "time"
            | "year"
            | "yearmonth"
            | "duration"
            | "list"
            | "array"
            | "object"
            | "geopoint"
        ):
            return pl.String
        case "number":
            return pl.Float64
        case "integer":
            return pl.Int64
        case _:
            return pl.String

import polars as pl

from seedcase_sprout.core.properties import FieldType

# Mapping from Frictionless data types to Polars data types.
# See https://sprout.seedcase-project.org/docs/design/interface/data-types
# for more information.
FRICTIONLESS_TO_POLARS: dict[FieldType, pl.DataType] = {
    "string": pl.String,
    "boolean": pl.Boolean,
    "integer": pl.Int64,
    "number": pl.Float64,
    "year": pl.Int32,
    "datetime": pl.Datetime,
    "date": pl.Date,
    "time": pl.Time,
    "yearmonth": pl.Date,
    "geopoint": pl.Array(pl.Float64, 2),
    "duration": pl.String,
    "object": pl.String,
    "array": pl.String,
    "geojson": pl.String,
    "any": pl.String,
}

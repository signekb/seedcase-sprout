"""File with read_csv_file and related functions."""
import csv
import os
from typing import Any

import polars as pl
from polars import Boolean, DataFrame, Series, read_csv


def read_csv_file(csv_file_path: str, row_number: int = 500) -> DataFrame:
    """Reads a CSV file and returns a polars.DataFrame with derived types.

    The property `dtypes` in the returned DataFrame contains the column/series
    types.

    It uses `polars.csv_read()`, but adds additional functionality:
    - Converts boolean-ish values (Yes, y, 1) to booleans
    - Finds CSV dialect of file and converts to a csv format suitable for
      `polars.csv_read()`, i.e. removes whitespaces and quotes

    Args:
        csv_file_path: The path of the CSV file to read
        row_number: The number of rows to scan from the file

    Returns:
        DataFrame: A `polars.DataFrame` with column types in `dtypes`.
    """
    transformed_csv = create_compatible_csv_file(csv_file_path, row_number)
    df = read_csv(transformed_csv, n_rows=row_number, try_parse_dates=True)
    os.remove(transformed_csv)

    return df.select([_convert_to_booleans_if_possible(column) for column in df])


def create_compatible_csv_file(csv_file_path: str, row_number: int):
    """Removes whitespace and quotes and overwrites csv."""
    # Find dialect
    with open(csv_file_path, "r") as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(10000))

    df = pl.read_csv(
        csv_file_path,
        infer_schema_length=0,
        separator=dialect.delimiter,
        n_rows=row_number,
    )
    df = df.select(pl.all().str.strip_chars())
    df = df.select(pl.all().name.map(lambda n: n.strip().strip('"')))
    df = df.select(pl.all().str.strip_chars('"'))
    cleaned_path = csv_file_path + "cleaned"
    df.write_csv(cleaned_path)
    return cleaned_path


BOOLEAN_MAPPING = {
    "yes": True,
    "Yes": True,
    "y": True,
    "Y": True,
    "no": False,
    "No": False,
    "n": False,
    "N": False,
    "": None,
}


def _convert_to_booleans_if_possible(series: Series) -> Series:
    """Converts series with boolean-ish values to actual booleans if possible.

    E.g. A "String" column with ("Yes", "y", "no", "n") is converted to
    (True, True, False, False)

    Args:
        series: Polars Series or a column

    Returns:
        Series: A Series converted to booleans if possible or the original series.
    """
    if _check_series_values(series, [0, 1]):
        return series.cast(Boolean)
    elif _check_series_values(series, list(BOOLEAN_MAPPING.keys())):
        return series.map_dict(BOOLEAN_MAPPING)

    return series


def _check_series_values(series: Series, allowed_values: list[Any]) -> bool:
    """Checks if a series only contains the allowed values and null values.

    This is relevant check before converting to a certain type. E.g. if
    all values are either 0 or 1, then we can convert to booleans

    Args:
        series: A series of values, which should be checked
        allowed_values: The allowed values.

    Returns:
        bool: True if series only contains values in `allowed_values` or null;
              False if series contains one or more values not in `allowed_values`

    """
    allowed_values_series = Series(allowed_values)
    if series.dtype != allowed_values_series.dtype:
        return False

    # Count allowed and null values
    value_match_count = series.is_in(allowed_values_series).sum()
    null_count = series.is_null().sum()
    return null_count + value_match_count == len(series)

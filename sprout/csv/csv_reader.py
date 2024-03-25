"""File with read_csv_file and related functions."""
import csv
import os
from typing import Any

import polars as pl
from polars import DataFrame, Series, read_csv


def read_csv_file(csv_file_path: str, row_count: int | None = 500) -> DataFrame:
    """Reads a CSV file and returns a polars.DataFrame with derived types.

    The property `dtypes` in the returned DataFrame contains the column/series
    types.

    It uses `polars.csv_read()`, but adds additional functionality:
    - Converts boolean-ish values (Yes, y, 1) to booleans
    - A preparation step removes whitespace and quotes, which is not handled
      natively by `polars.csv_read()`

    Args:
        csv_file_path: The path of the CSV file to read
        row_count: The number of rows to scan from the file. 'None' means all

    Returns:
        DataFrame: A `polars.DataFrame` with column types in `dtypes`.
    """
    transformed_csv = _transform_to_suitable_csv_format(csv_file_path, row_count)
    df = read_csv(transformed_csv, n_rows=row_count, try_parse_dates=True)
    os.remove(transformed_csv)

    return df


def _transform_to_suitable_csv_format(csv_path: str, row_count: int | None) -> str:
    """Removes whitespace+quotes and handles boolean-ish values in CSV file.

    This function is designed to preprocess CSV files for compatibility with
    `polars.read_csv()`, which may not correctly handle whitespace and quotes.
    Furthermore, it transforms boolean-ish values to actual booleans.

    For instance, it will transform:

        "name",     "city",     "age", "is_adult"
        "Phil",     "Aarhus",   "36",  "yes"

    into:

        name,city,age,is_adult
        Phil,Aarhus,36,True

    This ensures that column names and values are correctly identified and typed by
    `polars.read_csv()`.

    Args:
        csv_path: The path of the CSV file to transform.
        row_count: The number of rows to process in the CSV file. 'None' means all

    Returns:
        PathLike: The path to the transformed CSV file.
    """
    # Find dialect
    with open(csv_path, "r") as csv_file:
        try:
            dialect = csv.Sniffer().sniff(csv_file.read(10000))
        except csv.Error as e:
            raise csv.Error("Invalid CSV. " + e.args[0])

    if dialect.delimiter not in (",", ";", " ", "\t"):
        raise csv.Error(
            f"Invalid CSV. Use comma, semicolon, space or tab as "
            f"delimiter. Found delimiter: '{dialect.delimiter}'"
        )

    # Read csv without inferring types
    df = pl.read_csv(
        csv_path, infer_schema_length=0, separator=dialect.delimiter, n_rows=row_count
    )

    if len(df) == 0:
        raise csv.Error("Invalid CSV. No rows found!")

    df = df.select(pl.all().str.strip_chars())
    df = df.select(pl.all().name.map(lambda n: n.strip().strip('"')))
    df = df.select(pl.all().str.strip_chars('"'))

    df = df.select([_convert_decimal_with_comma_to_dot(column) for column in df])
    df = df.select([_convert_to_booleans_if_possible(column) for column in df])

    cleaned_path = csv_path + "cleaned"
    df.write_csv(cleaned_path)
    return cleaned_path


BOOLEAN_MAPPING = {
    "1": True,
    "yes": True,
    "Yes": True,
    "y": True,
    "Y": True,
    "no": False,
    "No": False,
    "n": False,
    "N": False,
    "0": False,
    "": None,
}


def _convert_decimal_with_comma_to_dot(series: pl.Series) -> pl.Series:
    # Replace decimal with ',' with '.'
    decimal_comma_regex = r"(\d+),(\d+)"
    empty_count = series.is_null().sum()
    match_count = series.str.count_matches(decimal_comma_regex).sum()
    if empty_count + match_count == len(series):
        return series.str.replace_all(decimal_comma_regex, "${1}.${2}")

    return series


def _convert_to_booleans_if_possible(series: Series) -> Series:
    """Converts series with boolean-ish values to actual booleans if possible.

    E.g. A "String" column with ("Yes", "y", "no", "n") is converted to
    (True, True, False, False)

    Args:
        series: Polars Series or a column

    Returns:
        Series: A Series converted to booleans if possible or the original series.
    """
    if _check_series_values(series, list(BOOLEAN_MAPPING.keys())):
        return series.replace(BOOLEAN_MAPPING, default=None)

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

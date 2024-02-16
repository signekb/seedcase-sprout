"""File with read_csv_file and related functions."""
import csv
import io
from typing import Any, TextIO

from polars import Boolean, DataFrame, Series, read_csv


def read_csv_file(csv_file: TextIO, row_number: int = 500) -> DataFrame:
    """Reads a CSV file and returns a polars.DataFrame with derived types.

    The property `dtypes` in the returned DataFrame contains the column/series
    types.

    It uses `polars.csv_read()`, but adds additional functionality:
    - Converts boolean-ish values (Yes, y, 1) to booleans
    - Finds CSV dialect of file and converts to a csv format suitable for
      `polars.csv_read()`, i.e., transform dialect to semicolon remove and
      whitespaces and quotes

    Args:
        csv_file (TextIO): The CSV file to read
        row_number (int, optional): The number of rows to scan from the file

    Returns:
        DataFrame: A `polars.DataFrame` with column types in `dtypes`.
    """
    csv_file = _transform_to_suitable_csv_format(csv_file, row_number)
    df = read_csv(csv_file, n_rows=row_number, try_parse_dates=True, separator=";")

    return df.select([_convert_to_booleans_if_possible(column) for column in df])


def _transform_to_suitable_csv_format(csv_file: TextIO, row_number: int = 500) -> TextIO:
    """Preparing the CSV content for polar.read_csv method.

    This function converts from any CSV dialect/format into a semicolon separated 
    format and strips whitespaces and quotes.

    Args:
        csv_file: A CSV file with a dialect that is potentially not suitable
                  for `polars.read_csv()`
        row_number: The number of rows used to infer csv dialect

    Returns:
        TextIO: An in-memory CSV file which is suitable for `polars.read_csv()`
    """
    # Read part of csv_file to detect dialect and return to beginning of file
    dialect = csv.Sniffer().sniff(csv_file.read(row_number))
    csv_file.seek(0)

    csv_content = ""
    for line in csv.reader(csv_file, dialect=dialect):
        csv_content = csv_content + ";".join(line) + "\n"
    return io.StringIO(csv_content)


BOOLEAN_MAPPING = {
    "yes": True,
    "Yes": True,
    "y": True,
    "Y": True,
    "no": False,
    "No": False,
    "n": False,
    "N": False,
}


def _convert_to_booleans_if_possible(series: Series) -> Series:
    """Converts series with boolean-ish values to actual booleans if possible.

    E.g. A "String" column with ("Yes", "y", "no", "n") is converted to
    (True, True, False, False)

    Args:
        series (Series): Polars Series or a column

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
        series (Series): A series of values, which should be checked
        allowed_values (list[Any]): The allowed values.

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

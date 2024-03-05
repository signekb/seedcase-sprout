"""CSV file validator."""
from typing import Mapping

import polars as pl
from polars import read_csv

from sprout.csv_reader import _transform_to_suitable_csv_format


class CsvValidationError:
    """Information about a CSV validation error."""

    def __init__(self, column: str, data_type: str, row_number: int, value: str):
        """Constructor.

        Args:
            column: Name of the column with the error
            data_type: The expected data type of the column
            row_number: The row of the error
            value: The value that gave an error
        """
        self.column = column
        self.data_type = data_type
        self.row_number = row_number
        self.value = value

    def __str__(self):
        """String representation of the CsvValidationError."""
        return (
            f"Value '{self.value}' is not '{self.data_type}'. Column: "
            f"'{self.column}', row: '{self.row_number}'"
        )


def validate_csv(
    file_path: str, dtypes: Mapping[str, pl.PolarsDataType]
) -> list[CsvValidationError]:
    """Validate the CSV file."""
    transformed_csv = _transform_to_suitable_csv_format(file_path, None)

    df = read_csv(transformed_csv, dtypes=dtypes, ignore_errors=True)

    df_strings = read_csv(transformed_csv, infer_schema_length=0)
    df_strings = df_strings.with_row_index("row_number", offset=1)

    return [error for col in df for error in get_errors(col, df_strings)]


def get_errors(column: pl.Series, df_strings: pl.DataFrame) -> list[CsvValidationError]:
    """Get the errors from the CSV file."""
    column_with_nulls = column.is_null()
    string_values = df_strings[column.name].filter(column_with_nulls)
    row_numbers = df_strings["row_number"].filter(column_with_nulls)
    return [
        CsvValidationError(
            column.name, str(column.dtype.base_type()), row_numbers[idx], val
        )
        for idx, val in enumerate(string_values)
        if val is not None
    ]

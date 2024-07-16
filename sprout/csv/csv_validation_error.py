"""CsvValidationError file."""

import polars as pl


class CsvValidationError:
    """Information about a CSV validation error."""

    def __init__(
        self,
        column: str,
        data_type: pl.DataType,
        row_number: int = 0,
        value: str = "",
        is_column_missing: bool = False,
    ):
        """CsvValidationError constructor.

        Args:
            column: Name of the column with the error
            data_type: The expected data type of the column
            row_number: The row of the error
            value: The value that gave an error
            is_column_missing: True if the entire column is missing
        """
        self.column = column
        self.data_type = str(data_type.base_type())
        self.row_number = row_number
        self.value = value
        self.is_column_missing = is_column_missing

    def __str__(self):
        """String representation of the CsvValidationError."""
        if self.is_column_missing:
            return f"Column '{self.column}' with type '{self.data_type}' is missing"

        return (
            f"Value '{self.value}' is not '{self.data_type}'. Column: "
            f"'{self.column}', row: '{self.row_number}'"
        )

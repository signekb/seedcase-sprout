from pathlib import Path

import polars as pl

from seedcase_sprout.core.internals import _check_is_file


def read_csv(data_path: Path) -> pl.DataFrame:
    """Loads data in the given CSV file into a Polars data frame.

    Args:
        data_path: The path to the CSV file.

    Returns:
        The Polars data frame.

    Raises:
        FileNotFoundError: If the file cannot be found or the path doesn't point to
            a file.
        ValueError: If the file is not a CSV file.
        pl.exceptions.NoDataError: If the file is empty.
        pl.exceptions.ComputeError: If the data cannot be loaded into a data frame.
        ValueError: If the data has a row that is longer than the header row.
    """
    _check_is_file(data_path)
    if data_path.suffix != ".csv":
        raise ValueError(f"{data_path} is not a CSV file.")

    try:
        return pl.read_csv(
            data_path,
            has_header=True,
            # Doesn't work all the time, and we want to use properties anyway.
            infer_schema=False,
            # Set as empty string since it will be easier to match with Frictionless.
            missing_utf8_is_empty_string=True,
        )
    except pl.exceptions.ComputeError as error:
        if "found more fields than defined" in str(error):
            raise ValueError(
                f"At least one row in the data file at {data_path} contains more items "
                "than the expected number of columns. Please make sure that all rows "
                "have the same number of items."
            ) from error
        raise

from pathlib import Path

import polars as pl
from polars.testing import assert_frame_equal
from pytest import fixture, raises

from seedcase_sprout.core.read_csv import read_csv


@fixture
def data_path(tmp_path) -> Path:
    return tmp_path / "data.csv"


def test_throws_error_if_file_not_found(data_path):
    """Should throw an error if the file cannot be found."""

    with raises(FileNotFoundError):
        read_csv(data_path)


def test_throws_value_error_if_file_not_csv(tmp_path):
    """Should throw a ValueError if the file is not a CSV file."""
    path = tmp_path / "data.txt"
    path.write_text("id,name\n1,Cassidy\n2,James\n3,Björn\n")

    with raises(ValueError):
        read_csv(path)


def test_throws_error_if_file_empty(data_path):
    """Should throw an error if the file is empty."""
    data_path.touch()

    with raises(pl.exceptions.NoDataError):
        read_csv(data_path)


def test_throws_error_if_data_cannot_be_loaded(data_path):
    """Should throw an error if the data cannot be loaded into a data frame."""
    data_path.write_text('name\n"This quote is not escaped')

    with raises(pl.exceptions.ComputeError):
        read_csv(data_path)


def test_schema_and_data_read_correctly(data_path):
    """Should return a data frame with the expected schema and data."""
    df = pl.DataFrame(
        {"id": [1, 2, 3], "name": ["Cassidy", "James", "Björn"]},
        schema={"id": pl.String, "name": pl.String},
        strict=False,
    )
    df.write_csv(data_path)

    df_read = read_csv(data_path)

    assert_frame_equal(df, df_read)


def test_nulls_read_as_empty_string(data_path):
    """Should read null values as empty strings."""
    df = pl.DataFrame(
        {"id": [1, 2, 3], "name": [None] * 3},
        schema={"id": pl.String, "name": pl.String},
        strict=False,
    )
    df.write_csv(data_path)

    df_read = read_csv(data_path)
    null_column = df_read.get_column("name").to_list()

    assert null_column == [""] * 3


def test_default_value_for_missing_column_is_empty_string(data_path):
    """When a row has no value for a column (not even null), the default value in the
    data frame should be an empty string."""
    data_path.write_text("id,name,age\n1,Cassidy\n2,James\n3,Björn\n")

    df_read = read_csv(data_path)
    missing_column = df_read.get_column("age").to_list()

    assert missing_column == [""] * 3


def test_throws_value_error_if_data_row_longer_than_header(data_path):
    """Should throw ValueError if the data has a row that is longer than the header."""
    data_path.write_text("id,name\n1,Cassidy\n2,James,33\n3,Björn\n")

    with raises(ValueError):
        read_csv(data_path)

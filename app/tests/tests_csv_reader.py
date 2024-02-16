"""File with tests for `csv_read_file()`."""
import csv
import datetime
import io
from typing import Any
from unittest import TestCase

from polars import DataFrame, Series

from app.csv_reader import read_csv_file


class CsvTests(TestCase):
    """Class with tests for `read_csv_file()`."""

    def test_csv_with_simple_types(self):
        """Testing that `read_csv_file()` should derive column types.

        For this example, "i1" as integer, "f1" as float and "b1" as a boolean.
        The values are also verified.
        """
        csv_file = io.StringIO(
            "i1,f1,b1\n" "1,2.3,true\n" "2,2.4,false\n" "3,2.6,false"
        )

        df = read_csv_file(csv_file)

        self.assert_types(df, "Int64", "Float64", "Boolean")
        self.assert_values(df["i1"], 1, 2, 3)
        self.assert_values(df["f1"], 2.3, 2.4, 2.6)
        self.assert_values(df["b1"], True, False, False)

    def test_csv_file_with_bytes(self):
        """Testing that `read_csv_file()` should derive column types.

        For this example, "i1" as integer, "f1" as float and "b1" as a boolean.
        The values are also verified.
        """
        csv_file = io.BytesIO(b"i1,f1,b1\n1,2.3,true\n2,2.4,false\n3,2.6,false")

        df = read_csv_file(csv_file)

        self.assert_types(df, "Int64", "Float64", "Boolean")

    def test_csv_with_semicolon_and_whitespace(self):
        """Testing a csv dialect with semicolon and initial whitespace."""
        csv_file = io.StringIO(
            "i1;    f1;     b1;     s1\n"
            "10;    5.3;    True;   Hi\n"
            "11;    1.0;    False;  Hello\n"
            "12;    1;      False;  Man"
        )

        df = read_csv_file(csv_file)

        self.assert_types(df, "Int64", "Float64", "Boolean", "String")
        self.assert_values(df["i1"], 10, 11, 12)
        self.assert_values(df["f1"], 5.3, 1, 1)
        self.assert_values(df["b1"], True, False, False)
        self.assert_values(df["s1"], "Hi", "Hello", "Man")

    def test_csv_with_semicolon_and_quotes(self):
        """Testing dialect with quotes, semicolon and initial whitespace."""
        csv_file = io.StringIO(
            '"i1";  "f1";   "b1";       "s1"\n'
            '"10";  "5.3";  "True";     "Hi, Man"\n'
            '"11";  "1.0";  "False";    "Hello?"\n'
            '"12";  "1";    "False";    "What, about"'
        )

        df = read_csv_file(csv_file)

        self.assert_types(df, "Int64", "Float64", "Boolean", "String")
        self.assert_values(df["s1"], "Hi, Man", "Hello?", "What, about")

    def test_boolean_ish_values(self):
        """Column with boolean-ish/empty values should convert to booleans."""
        csv_file = io.StringIO(
            "b1,    b2,     b3,     b4\n"
            "0,     true,   yes,    y\n"
            "1,     false,  no,     y\n"
            ",      false,  ,       n"
        )

        df = read_csv_file(csv_file)

        self.assert_types(df, "Boolean", "Boolean", "Boolean", "Boolean")
        self.assert_values(df["b1"], False, True, None)
        self.assert_values(df["b2"], True, False, False)
        self.assert_values(df["b3"], True, False, None)
        self.assert_values(df["b4"], True, True, False)

    def test_series_should_remain_if_series_has_some_none_boolean_values(self):
        """A column should remain if not all values are boolean-ish.

        So (0, 1, 2) remains an Int64 column and ("true", "REALLY TRUE!",
        "false") remains a String column
        """
        csv_file = io.StringIO(
            "s1,    s2\n" "0,     true\n" "1,     REALLY TRUE!\n" "2,     false"
        )

        df = read_csv_file(csv_file)

        self.assert_types(df, "Int64", "String")
        self.assert_values(df["s1"], 0, 1, 2)
        self.assert_values(df["s2"], "true", "REALLY TRUE!", "false")

    def test_datetime(self):
        """Testing different date and time formats.

        The columns (d1, d2, d3) should convert to dates and (t1) should
        convert to time

        NOTICE: d3 (ex: '27. Oct 1987') is not recognized as date
        """
        csv_file = io.StringIO(
            "d1,                    d2,         d3,             t1\n"
            "1987-10-27 00:00:00,   1987-10-27, 27. Oct 1987,   12:00:00\n"
            "2000-01-28 12:00:00,   2000-01-28, 28. Jan 2000,   13:00:01\n"
            "2024-07-01 12:00:01,   2024-07-01, 1. Jul 2024,    00:00:00"
        )

        df = read_csv_file(csv_file)

        self.assert_types(
            df, "Datetime(time_unit='us', time_zone=None)", "Date", "String", "Time"
        )
        self.assert_values(
            df["d1"],
            datetime.datetime.fromisoformat("1987-10-27"),
            datetime.datetime.fromisoformat("2000-01-28T12"),
            datetime.datetime.fromisoformat("2024-07-01T12:00:01"),
        )
        self.assert_values(
            df["d2"],
            datetime.date.fromisoformat("1987-10-27"),
            datetime.date.fromisoformat("2000-01-28"),
            datetime.date.fromisoformat("2024-07-01"),
        )
        self.assert_values(df["d3"], "27. Oct 1987", "28. Jan 2000", "1. Jul 2024")
        self.assert_values(
            df["t1"],
            datetime.time.fromisoformat("12:00:00"),
            datetime.time.fromisoformat("13:00:01"),
            datetime.time.fromisoformat("00:00:00"),
        )

    def test_wrongly_formatted_csv(self):
        """Testing a wrongly formatted CSV file.

        The row has three values but only two two columns - A csv.Error
        is expected
        """
        csv_file = io.StringIO("s1,s2\n" "Hello, World, Seedcase")

        self.assertRaises(csv.Error, read_csv_file, csv_file)

    def assert_types(self, df: DataFrame, *expected_types: str):
        """A method test `expected_types` in a DataFrame object.

        Args:
            df: The DataFrame with data and types
            *expected_types: a list of types we expect (in order)
        """
        self.assertEqual(len(df.columns), len(expected_types), "Missing columns!")
        for column_position in range(0, len(expected_types)):
            column_name = df.columns[column_position]
            column_type = str(df.dtypes[column_position])
            self.assertEqual(
                expected_types[column_position], column_type, "column:" + column_name
            )

    def assert_values(self, s: Series, *expected_values: Any):
        """Shorthand function to assert values series.

        Args:
            s: A Series is a column of data
            *expected_values: a list of types we expect (in order)
        """
        for value_position in range(0, len(s)):
            value = s[value_position]
            expected_value = expected_values[value_position]
            self.assertEqual(
                value, expected_value, s.name + ", row:" + str(value_position)
            )

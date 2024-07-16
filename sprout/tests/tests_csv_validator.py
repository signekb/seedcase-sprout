"""Testing CSV validator."""

import os
import tempfile
from unittest import TestCase

import polars as pl

from sprout.csv.csv_validator import validate_csv


class CsvValidatorTests(TestCase):
    def setUp(self) -> None:
        """Test setup."""
        self.temp_file = None

    def test_expects_ints_but_found_a_float(self):
        """Validation should fail as float is found in int column."""
        file = self.create_file("s1,i1\nA,1\nB,2.2")

        errors = validate_csv(file, {"s1": pl.String, "i1": pl.Int64})

        self.assertEqual(1, len(errors))
        self.assertEqual(
            "Value '2.2' is not 'Int64'. Column: 'i1', row: '2'", str(errors[0])
        )

    def test_should_fail_if_column_is_missing_in_csv(self):
        """Validation should fail as float is found in int column."""
        file = self.create_file("s1,i1\nA,1\nB,2")

        errors = validate_csv(file, {"s1": pl.String, "i1": pl.Int64, "i2": pl.Int64})

        self.assertEqual(1, len(errors))
        self.assertEqual("Column 'i2' with type 'Int64' is missing", str(errors[0]))

    def test_empty_int_value_is_okay(self):
        """Validation should not fail when a value is missing."""
        file = self.create_file("s,ints\nC,3\nD,")

        errors = validate_csv(file, {"s": pl.String, "ints": pl.Int64})

        self.assertEqual(0, len(errors))

    def test_boolean_ish_values(self):
        """Validation should not fail when using yes,no or 0,1 as booleans."""
        file = self.create_file("s,b1,b2\nA,yes,1\nD,no,0")
        expected_types = {"s": pl.String, "b1": pl.Boolean, "b2": pl.Boolean}

        errors = validate_csv(file, expected_types)

        self.assertEqual(0, len(errors))

    def test_dates(self):
        """Dates in the format 2024-01-01 should work."""
        file = self.create_file("i1,d1\n1,2024-01-01\n2,2024-01-02")
        expected_types = {"i1": pl.Int64, "d1": pl.Date}

        errors = validate_csv(file, expected_types)

        self.assertEqual(0, len(errors))

    def test_for_an_invalid_date(self):
        """An invalid date should create an error."""
        file = self.create_file("i1,d1\n1,2024-99-01\n2,2024-01-02")
        expected_types = {"i1": pl.Int64, "d1": pl.Date}

        errors = validate_csv(file, expected_types)

        self.assertEqual(1, len(errors))
        self.assertEqual("d1", errors[0].column)
        self.assertEqual("2024-99-01", errors[0].value)

    def create_file(self, content: str):
        """Creates temp file that is cleaned up in tearDown."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)

        self.temp_file.write(content.encode())
        self.temp_file.close()
        return self.temp_file.name

    def tearDown(self):
        """Clean up file."""
        if self.temp_file:
            self.temp_file.close()
            os.remove(self.temp_file.name)

"""Testing column datatypes."""

import datetime

import polars
from django.test import TestCase

from sprout.models import ColumnDataType


class ColumnDataTypeTests(TestCase):
    """Testing column datatypes."""

    def test_get_from_series_Decimal(self):
        """Series with float should return type: Decimal"""
        series = polars.Series("series", [1.1])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("Decimal", data_type.display_name)

    def test_get_from_series_WholeNumber(self):
        """Series with int should return type: Whole Number"""
        series = polars.Series("series", [1])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("Whole Number", data_type.display_name)

    def test_get_from_series_YesOrNo(self):
        """Series with booleans should return type: True/False"""
        series = polars.Series("series", [True])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("True/False", data_type.display_name)

    def test_get_from_series_Time(self):
        """Series with time should return type: Time"""
        series = polars.Series("series", [datetime.time()])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("Time", data_type.display_name)

    def test_get_from_series_Date(self):
        """Series with date should return type: Date"""
        series = polars.Series("series", [datetime.date.today()])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("Date", data_type.display_name)

    def test_get_from_series_DateTime(self):
        """Series with datetime should return type: Date+Time"""
        series = polars.Series("series", [datetime.datetime.now()])

        data_type = ColumnDataType.get_from_series(series)

        self.assertEqual("Date+Time", data_type.display_name)

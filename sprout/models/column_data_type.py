"""Module defining the ColumnDataType model and COLUMN_DATA_TYPES."""

from django.db import models
from polars import Series


class ColumnDataType(models.Model):
    """Model representing the data types of columns."""

    display_name = models.TextField()
    description = models.TextField()
    polars_types = models.TextField(default="")

    @staticmethod
    def get_from_series(series: Series) -> "ColumnDataType":
        """Finds ColumnDataType based on series dtype.

        Args:
            series: The polars.Series to find the  ColumnDataType from
        """
        series_polar_type = str(series.dtype.base_type())

        for data_type in COLUMN_DATA_TYPES:
            if series_polar_type in data_type.polars_types.split(","):
                return data_type

        raise ValueError("ColumnMetaData not found for :" + series_polar_type)

    def __str__(self):  # noqa: D105
        return self.display_name


"""
COLUMN_DATA_TYPES contains all the Sprout data types.

Changing the properties of this content can be risky. See the list below.

- NO RISK: It's safe to alter the `description` of the data types.
- LITTLE RISK: The `display_name` should rarely be changed. Changes might
  confuse users and should never change to a different type (Text -> Decimal)
- FORBIDDEN: `id`. You should never change the id, since this is used as foreign
"""
COLUMN_DATA_TYPES = [
    ColumnDataType(
        id=0,
        display_name="Decimal",
        polars_types="Decimal,Float32,Float64",
        description="Also known as a float or double precision. This field stores "
        "decimal numbers. Use this for items like height, blood glucose, or other "
        "measurements with high degrees of precision",
    ),
    ColumnDataType(
        id=1,
        display_name="Whole Number",
        polars_types="Int8,Int16,Int32,Int64,UInt8,UInt16,UInt32,UInt64",
        description="Also known as an integer. This field only allows whole numbers to "
        "be stored. Use this when you want to store data that doesn't need a decimal "
        "(e.g. number of people in a household)",
    ),
    ColumnDataType(
        id=2,
        display_name="Text",
        polars_types="String",
        description="A text field without a limit to how many characters can be stored",
    ),
    ColumnDataType(
        id=3,
        display_name="True/False",
        polars_types="Boolean",
        description="Also known as boolean or logical. Sprout stores this data type as True "
        "or False. If you need or want to store actual words, "
        "use the Text field.",
    ),
    ColumnDataType(
        id=4,
        display_name="Time",
        polars_types="Time",
        description="Stores time following the [ISO 8601](https://www.iso.org"
        "/iso-8601-date-and-time-format.html) format of `hh:mm:ss.ms` (hours, minutes, "
        "seconds, milliseconds)",
    ),
    ColumnDataType(
        id=5,
        display_name="Date+Time",
        polars_types="Datetime",
        description="Also known as DateTime or Timestamp. The field stores the date "
        "time following the "
        "[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format as "
        "`yyyy-mm-dd hh:mm:ss.ms` (year, month, day, hour, minutes, seconds, "
        "milliseconds)",
    ),
    ColumnDataType(
        id=6,
        display_name="Date",
        polars_types="Date",
        description="This field only stores dates, following the [ISO 8601]"
        "(https://www.iso.org/iso-8601-date-and-time-format.html) "
        "format of `yyyy-mm-dd` (year, month, day)",
    ),
]


def update_column_data_types(**kwargs) -> None:
    """Creates or updates all ColumnDataType based on COLUMN_DATA_TYPES.

    This is executed on app startup just after the migrations are completed.
    This method is used in AppConfig.ready()

    Args:
        **kwargs: A required argument by the Django, but it is not used
    """
    print("ColumnDataType updated")
    ColumnDataType.objects.bulk_create(COLUMN_DATA_TYPES, ignore_conflicts=True)
    fields = ["display_name", "description", "polars_types"]
    ColumnDataType.objects.bulk_update(COLUMN_DATA_TYPES, fields=fields)

from typing import Any

from django.db import models


class ColumnDataType(models.Model):
    display_name = models.TextField()
    description = models.TextField()
    python_type = models.TextField()
    pandas_type = models.TextField()


def update_column_data_types(*_: Any) -> None:
    """
    Method to be used in a migration when the content in the list called ColumnDataTypes
    is changed in any way.

    Follow the ColumnDataTypes docstring when you want to change the content
    of ColumnDataType

    Args:
        *_: An argument which is not used but required in
    """
    ColumnDataType.objects.bulk_create(ColumnDataTypes, ignore_conflicts=True)
    fields = ['display_name', 'description', 'python_type', 'pandas_type']
    ColumnDataType.objects.bulk_update(ColumnDataTypes, fields=fields)


def fake_reverting_method(*_: Any):
    print("Reverting ")


"""
When the sprout types are changed, you need to add a new migration.
You create a migration with:

python manage.py makemigrations

A migration file is added in the migrations folder. Add the following
line at the end of the file:

migrations.RunPython(update_column_data_types, fake_reverting_method)

This will create or update the ColumnDataTypes defined in Types.
(See 00001_initial.py to get inspiration)
"""
ColumnDataTypes = [
    ColumnDataType(id=0, display_name="Decimal",
                   description="Also known as a Float or Double Precision. This field stores decimal numbers. Use this for items like height, blood glucose, or other measurements with high degrees of precision",
                   pandas_type="float64", python_type="float"),
    ColumnDataType(id=1, display_name="Whole Number", pandas_type="int64",python_type="int",
                   description="Also known as an `integer`. This field only allows whole numbers to be stored. Use this when you want to store data that doesn't need a decimal (e.g. number of people in a household)"),
    ColumnDataType(id=2, display_name="Text",
                   description="A text field without a limit to how many characters can be stored",
                   pandas_type="object", python_type="str"),
    ColumnDataType(id=3, display_name="Yes/No",
                   description="Also known as Yes/No, Boolean, or Logical. This stores data as either 0/1 or True/False. If you need/want to store actual words, use the Text field",
                   pandas_type="bool",
                   python_type="bool"),
    ColumnDataType(id=4, display_name="Time",
                   description="Stores time following the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format of `hh:mm:ss.ms` (hours, minutes, seconds, milliseconds)",
                   pandas_type="timedelta64[ns]",
                   python_type="timedelta"),
    ColumnDataType(id=5, display_name="Date+Time",
                   description="Also known as DateTime or Timestamp. The field stores the date time following the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format as `yyyy-mm-dd hh:mm:ss.ms` (year, month, day, hour, minutes, seconds, milliseconds)",
                   pandas_type="datetime64[ns]",
                   python_type="datetime")
]

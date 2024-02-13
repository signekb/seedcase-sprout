from django.shortcuts import render

# Split views.py into multiple files is based on:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html
from .file_upload import file_upload
from .column_review import (
    column_review,
    columndata_review,
    update_column_metadata,
    update_columns_for_table,
)
from .data_import import data_import


def home(request):
    return render(request, "home.html")

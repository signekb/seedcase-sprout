from django.shortcuts import render

# Split views.py into multiple files is based on:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html
from .file_upload import file_upload
from .column_review import column_view


def home(request):
    return render(request, "home.html")


def data_import(request):
    return render(request, "data-import.html")

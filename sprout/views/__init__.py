"""Module with all views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Split views.py into multiple files is based on:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html
from .column_review import (
    column_review,
)
from .project_id_data_id_metadata_edit_grid import (
    project_id_data_id_metadata_edit_grid,
)
from .project_id_view import project_id_view
from .metadata_create import metadata_create
from .table_files import table_file_download, table_files


def home(request: HttpRequest) -> HttpResponse:
    """Renders the Sprout landing page.

    Args:
        request: The HttpRequest from the user

    Returns:
        HttpResponse: HTML content for the landing page.
    """
    return render(request, "index.html")

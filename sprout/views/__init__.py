"""Module with all views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .projects_id_data_id_metadata_create import projects_id_data_id_metadata_create
from .projects_id_data_id_metadata_edit_grid import (
    projects_id_data_id_metadata_edit_grid,
)

# Split views.py into multiple files is based on:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/02/how-to-split-views-into-multiple-files.html
from .projects_id_data_id_metadata_edit_table import (
    projects_id_data_id_metadata_edit_table,
)
from .projects_id_view import projects_id_view
from .table_files import table_file_download, table_files


def home(request: HttpRequest) -> HttpResponse:
    """Renders the Sprout landing page.

    Args:
        request: The HttpRequest from the user

    Returns:
        HttpResponse: HTML content for the landing page.
    """
    return render(request, "index.html")

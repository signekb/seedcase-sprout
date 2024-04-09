"""Module with all views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .projects_id_metadata_create import projects_id_metadata_create
from .projects_id_metadata_id_data_update import projects_id_metadata_id_data_update
from .projects_id_metadata_id_update import projects_id_metadata_id_update
from .projects_id_metadata_view import projects_id_metadata_view
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

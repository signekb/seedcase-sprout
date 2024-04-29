"""File with data_import view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def projects_id_view(request: HttpRequest) -> HttpResponse:
    """Landing page for the project.

    Args:
        request (HttpRequest): Contains metadata about the request

    Returns:
        HttpResponse: A rendered project overview.
    """
    return render(request=request, template_name="projects-id-view.html")

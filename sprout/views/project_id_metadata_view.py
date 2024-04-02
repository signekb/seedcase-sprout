"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from sprout.models import ColumnMetadata, TableMetadata


def project_id_metadata_view(request: HttpRequest) -> HttpResponse:
    """View the existing metadata in a project.

    Either create new metadata, edit existing metadata, or upload new data.

    Args:
        request: The HTTP request object that contains metadata about the request.

    Returns:
        HTTP response that either renders the project-id-metadata page or redirects
        to create new metadata, edit existing metadata, or upload new data.
    """
    existing_metadata = TableMetadata.objects.all()

    return render(
        request,
        "project-id-metadata-view.html",
        {
            "existing_metadata": existing_metadata,
        },
    )

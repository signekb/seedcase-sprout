"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from sprout.app.models import Tables


def projects_id_metadata_view(request: HttpRequest) -> HttpResponse:
    """View the existing metadata in a project.

    Either create new metadata, update existing metadata, or upload new data.

    Args:
        request: The HTTP request object that contains metadata about the request.

    Returns:
        HTTP response that either renders the projects-id-metadata page or redirects
        to create new metadata, update existing metadata, or upload new data.
    """
    # Columns for each table are prefetched and can be accessed in the Django template
    # using 'table.columns_set.all'
    existing_metadata = Tables.objects.prefetch_related("columns_set").all()

    return render(
        request=request,
        template_name="projects-id-metadata-view.html",
        context={"existing_metadata": existing_metadata},
    )

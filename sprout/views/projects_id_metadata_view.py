"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sprout.forms import TableMetadataForm
from sprout.models import ColumnMetadata, TableMetadata


def projects_id_metadata_view(request: HttpRequest) -> HttpResponse:
    """View the existing metadata in a project.

    Either create new metadata, update existing metadata, or upload new data.

    Args:
        request: The HTTP request object that contains metadata about the request.

    Returns:
        HTTP response that either renders the projects-id-metadata page or redirects
        to create new metadata, update existing metadata, or upload new data.
    """
    existing_metadata = TableMetadata.objects.all()
    existing_metadata_columns = ColumnMetadata.objects.all()

    # if POST, process the data in form (only happens when creating new metadata)
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(data=request.POST)

        # if input passes validation, save form and redirect to file upload
        if form.is_valid():
            table_metadata = form.save()

            return redirect(
                to=reverse(
                    "projects-id-metadata-create",
                    kwargs={"table_id": table_metadata.id},
                )
            )

    # if GET (or any other method), create a blank form
    else:
        form = TableMetadataForm(data=None)

    return render(
        request=request,
        template_name="projects-id-metadata-view.html",
        context={
            "existing_metadata": existing_metadata,
            "existing_metadata_columns": existing_metadata_columns,
            "form": form,
        },
    )

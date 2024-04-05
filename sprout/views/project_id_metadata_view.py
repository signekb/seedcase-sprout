"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from sprout.forms import TableMetadataForm
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

    # create a dictionary of existing metadata columns to filter in the template
    dict_existing_metadata_columns = {}

    for column in ColumnMetadata.objects.all():
        if column.table_metadata.pk not in dict_existing_metadata_columns:
            dict_existing_metadata_columns[column.table_metadata.pk] = []
        dict_existing_metadata_columns[column.table_metadata.pk].append(column)

    # if POST, process the data in form (only happens when creating new metadata)
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(data=request.POST)

        # if input passes validation, save form and redirect to file upload
        if form.is_valid():
            table_metadata = form.save()

            return redirect(to=f"metadata/create/{table_metadata.id}")

    # if GET (or any other method), create a blank form
    else:
        form = TableMetadataForm(data=None)

    return render(
        request=request,
        template_name="project-id-metadata-view.html",
        context={
            "existing_metadata": existing_metadata,
            "existing_metadata_columns": dict_existing_metadata_columns,
            "form": form,
        },
    )

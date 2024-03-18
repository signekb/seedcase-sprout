"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from sprout.models import ColumnMetadata, TableMetadata


def view_existing_tables(
    request: HttpRequest, selected_table: int | None = None
) -> HttpResponse:
    """View the existing data in a project.

    Either create new metadata based on existing data,
    edit metadata of existing data, or upload new data.

    Args:
        request: The HTTP request object that contains metadata about the request.
        selected_table: The identifier of the selected data. Defaults to None.

    Returns:
        HTTP response that either renders the view-existing-tables page or redirects
        to create new metadata, edit metadata, or upload new data.
    """
    table_metadata = TableMetadata.objects.all()
    selected_table_id = request.GET.get("selected_table_id")

    if request.method == "POST":
        # TODO: Add correct redirect for each button
        if "button_create" in request.POST:
            return redirect("/file-upload/" + str(selected_table_id))
        elif "button_edit" in request.POST:
            return redirect("/file-upload/" + str(selected_table_id))
        elif "button_upload" in request.POST:
            return redirect("/file-upload/" + str(selected_table_id))

    return render(
        request,
        "view-existing-tables.html",
        {
            "existing_tables": table_metadata,
            "selected_table_id": selected_table_id,
        },
    )


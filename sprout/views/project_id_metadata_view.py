"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

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
    selected_metadata_id = request.GET.get("selected_metadata_id")
    selected_metadata_columns = ColumnMetadata.objects.filter(
        table_metadata_id=selected_metadata_id
    )
    msg_edit_upload_wo_selected_row = None

    if request.method == "POST":
        # TODO: Add correct redirect for each button
        if "button_create" in request.POST:
            return redirect("/data-import")

        elif "button_edit" in request.POST and selected_metadata_id is not None:
            return redirect("/column-review/" + str(selected_metadata_id))

        elif "button_upload" in request.POST and selected_metadata_id is not None:
            return redirect("/column-review/" + str(selected_metadata_id))

    return render(
        request,
        "project-id-metadata-view.html",
        {
            "existing_metadata": existing_metadata,
            "selected_metadata_id": selected_metadata_id,
            "selected_metadata_columns": selected_metadata_columns,
            "msg_edit_upload_wo_selected_row": msg_edit_upload_wo_selected_row,
        },
    )

"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from sprout.models import TableMetadata


def project_id_data(
    request: HttpRequest, selected_table: int | None = None
) -> HttpResponse:
    """View the existing data in a project.

    Either create new metadata based on existing data,
    edit metadata of existing data, or upload new data.

    Args:
        request: The HTTP request object that contains metadata about the request.
        selected_table: The identifier of the selected data. Defaults to None.

    Returns:
        HTTP response that either renders the project-id-data page or redirects
        to create new metadata, edit metadata, or upload new data.
    """
    existing_metadata = TableMetadata.objects.all()
    selected_metadata_id = request.GET.get("selected_metadata_id")
    msg_edit_upload_wo_selected_row = None

    if request.method == "POST":
        # TODO: Add correct redirect for each button
        if "button_create" in request.POST:
            return redirect("/data-import")
        elif "button_edit" in request.POST:
            if selected_metadata_id is None:
                msg_edit_upload_wo_selected_row = (
                    "To edit metadata or upload data, you must select a table"
                )
            else:
                return redirect("/column-review/" + str(selected_metadata_id))
        elif "button_upload" in request.POST:
            if selected_metadata_id is None:
                msg_edit_upload_wo_selected_row = (
                    "To edit metadata or upload data, you must select a table"
                )
            else:
                return redirect("/column-review/" + str(selected_metadata_id))

    return render(
        request,
        "project-id-data.html",
        {
            "existing_metadata": existing_metadata,
            "selected_metadata_id": selected_metadata_id,
            "msg_edit_upload_wo_selected_row": msg_edit_upload_wo_selected_row,
        },
    )

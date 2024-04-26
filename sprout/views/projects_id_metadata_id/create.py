from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from sprout.views.projects_id_metadata_id.step_columns_update import step_columns_update
from sprout.views.projects_id_metadata_id.step_confirmation import step_confirmation
from sprout.views.projects_id_metadata_id.step_file_upload import step_file_upload
from sprout.views.projects_id_metadata_id.step_name_and_description import \
    step_name_and_description


def projects_id_metadata_create(
    request: HttpRequest,
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating metadata for data."""
    table_id = int(request.GET["table_id"]) if "table_id" in request.GET else None

    # Step 2
    if request.GET.get("step") == "2":
        return step_file_upload(request, table_id)

    # Step 3
    if request.GET.get("step") == "3":
        return step_columns_update(request, table_id)

    # Step 4
    if request.GET.get("step") == "4":
        return step_confirmation(request, table_id)

    # Step 1
    return step_name_and_description(request, table_id)

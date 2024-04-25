from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from sprout.views.projects_id_metadata_create_1 import projects_id_metadata_create_1
from sprout.views.projects_id_metadata_create_2 import projects_id_metadata_create_2
from sprout.views.projects_id_metadata_create_3 import projects_id_metadata_create_3
from sprout.views.projects_id_metadata_create_4 import projects_id_metadata_create_4


def projects_id_metadata_create(
    request: HttpRequest,
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating metadata for data."""
    table_id = int(request.GET["table_id"]) if "table_id" in request.GET else None

    # Step 2
    if request.GET.get("step") == "2":
        return projects_id_metadata_create_2(request, table_id)

    # Step 3
    if request.GET.get("step") == "3":
        return projects_id_metadata_create_3(request, table_id)

    # Step 4
    if request.GET.get("step") == "4":
        return projects_id_metadata_create_4(request, table_id)

    # Step 1
    return projects_id_metadata_create_1(request, table_id)

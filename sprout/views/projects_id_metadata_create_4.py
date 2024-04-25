from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def projects_id_metadata_create_4(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page final page when creating metadata table."""
    return render(request, "projects-id-metadata-create.html")

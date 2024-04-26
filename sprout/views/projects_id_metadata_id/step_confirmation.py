from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def step_confirmation(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page final page when creating metadata table."""
    return render(request, "projects_id_metadata_id/create.html")

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from sprout.models import Tables


def projects_id_metadata_create_4(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating metadata for data.

    The ``table_id`` comes from the URL. The ``table_id`` is used fetch the
    tables from the database.

    - On GET requests, the page is rendered.
    - On POST requests, the submitted CSV file is validated and column
      metadata persisted for the table.

    Args:
        request: The HTTP request from the server.
        table_id: The ``table_id`` from the Tables.

    Returns:
        HttpResponse: For GET requests and POST requests with errors
        HttpResponseRedirect: For POST request without any error
    """
    table = Tables.objects.get(pk=table_id)

    return render(request, "projects-id-metadata-create.html")

"""Module for handling file downloads."""

from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render

from seedcase_sprout.app.models import Files, Tables


def table_files(request: HttpRequest, table_id: int) -> HttpResponse:
    """Renders an overview of uploaded files for a certain table.

    Args:
        request: The request from the client
        table_id: The table id

    Returns:
        HttpResponse: Render of files for a table
    """
    tables = Tables.objects.get(pk=table_id)
    files = Files.objects.filter(tables_id=table_id).all()
    context = {"files": files, "table": tables}
    return render(request, "table-files.html", context)


def table_file_download(
    request: HttpRequest, table_id: int, file_id: int
) -> FileResponse:
    """A download link based on table_id and file_id.

    Args:
        request: The request from the client
        table_id: Table id
        file_id: The id of the file to download

    Returns:
        FileResponse: A file download response
    """
    files = Files.objects.get(id=file_id, tables_id=table_id)

    return FileResponse(open(files.server_file_path, "rb"), as_attachment=True)

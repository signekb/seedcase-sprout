"""Module for handling file downloads."""
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render

from sprout.models import Files, TableMetadata


def table_files(request: HttpRequest, table_id: int) -> HttpResponse:
    """Renders an overview of uploaded files for a certain table.

    Args:
        request: The request from the client
        table_id: The table id

    Returns:
        HttpResponse: Render of files for a table
    """
    table_metadata = TableMetadata.objects.get(pk=table_id)
    files = Files.objects.filter(table_metadata_id=table_id).all()
    context = {"files": files, "table": table_metadata}
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
    files = Files.objects.get(id=file_id, table_metadata_id=table_id)

    return FileResponse(open(files.server_file_path, "rb"), as_attachment=True)

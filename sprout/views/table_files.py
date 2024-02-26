"""Module for handling file downloads."""
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render

from sprout.models import TableMetadata
from sprout.models.file_metadata import FileMetaData


def table_files(request: HttpRequest, table_id: int) -> HttpResponse:
    """Overview of files for a table."""
    table_metadata = TableMetadata.objects.get(pk=table_id)
    files = FileMetaData.objects.filter(table_metadata_id=table_id).all()
    return render(
        request, "table-files.html", {"files": files, "table": table_metadata}
    )


def table_file_download(
    request: HttpRequest, table_id: int, file_id: int
) -> FileResponse:
    """Download of file based on a file_id."""
    # HERE WE CAN CHECK IF THE USER HAVE ACCESS
    file_metadata = FileMetaData.objects.get(id=file_id)
    print(file_metadata.server_file_path)

    return FileResponse(open(file_metadata.server_file_path, "rb"), as_attachment=True)

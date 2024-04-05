from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from sprout.models import FileMetadata, TableMetadata
import polars as pl


def project_id_metadata_id_data_update(
    request: HttpRequest, table_id: int
) -> HttpResponse:
    """Updates data in (or adds data to) a database table for a specific metadata object.

    Args:
        request: _description_
        table_id: _description_

    Returns:
        _description_
    """
    table_metadata = get_object_or_404(TableMetadata, id=table_id)
    context = {
        "upload_success": False,
        "table_name": table_metadata.name,
    }
    if request.method == "POST":
        new_uploaded_file = get_uploaded_file(request)
        file_metadata = FileMetadata.create_file_metadata(new_file, table_id)
        new_server_file = 
        schema = get_schema(id=table_id)
        # TODO: Read only most recently uploaded file
        data = read_csv_file(file_metadata.server_file_path, row_count=None)
        # verify_headers(data, schema)
        # verify_data_types(data, schema)
        # verify_data_types(data, schema)
        # if false delete uploaded file
        context = {
            "table_name": table_metadata.name,
            "upload_success": True,
            "file_metadata": file_metadata,
            "number_rows": count_rows(file_metadata.server_file_path),
        }

    # TODO: Provide context for response instead of redirect?
    # And button in template to move to other page?
    return render(request, "project-id-metadata-id-data-update.html", context)


def get_uploaded_file(request: HttpRequest) -> UploadedFile:
    """Get uploaded file name from request."""
    return request.FILES.get("uploaded_file")


def count_rows(path: str) -> int:
    # TODO: This might not always be a csv.
    data = pl.scan_csv(path)
    return data.select(pl.len()).collect().item()


def get_schema(id: int) -> FileMetadata:
    return ColumnMetadata.objects.get(pk=id)


new_data = read_raw_file(input_path)

# Inform if there are columns that exist in the uploaded data,
# that don't exist in the
verify_headers(data, schema)
verify_data_types(data, schema)

read_database(path, table_name)
database.join(other=new_data)  # from polars
create_path(...)
database.write_database(table_name=table_name, connection=path)

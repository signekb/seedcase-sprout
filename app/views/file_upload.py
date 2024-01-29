from typing import IO

from django.core.files.uploadhandler import StopUpload
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from app.models import ColumnMetadata, TableMetadata


def file_upload(request: WSGIRequest, table_id: str):
    if request.method == "POST":
        return handle_file_upload_post_request(request, table_id)

    return render_file_upload_page(request, table_id, "")


def handle_file_upload_post_request(request: WSGIRequest, table_id: str):
    try:
        validate_csv_and_save_columns(table_id, request.FILES)
    except StopUpload as upload_error:
        return render_file_upload_page(request, table_id, upload_error.args[0])

    return redirect("/edit-table-columns/" + str(table_id))


def render_file_upload_page(request: WSGIRequest, table_id: str, upload_error: str):
    table_metadata = TableMetadata.objects.get(pk=table_id)
    file_upload_data = {"table_name": table_metadata.name, "upload_error": upload_error}
    return render(request, "file-upload.html", file_upload_data)


def validate_csv_and_save_columns(table_id: str, files: list[IO]):
    uploaded_file = files.get("uploaded_file", None)

    if not uploaded_file.name.endswith(".csv"):
        error_msg = "Unsupported file format: ." + uploaded_file.name.split(".")[-1]
        raise StopUpload(error_msg)

    return extract_and_persist_column_metadata(table_id, uploaded_file)


def extract_and_persist_column_metadata(table_id: str, uploaded_file: IO):
    # A more complicated function needs to be added here
    column_names = uploaded_file.readline().decode("utf-8").split(",")

    if len(column_names) < 2:
        error_msg = "Unable to extract column headers. We need at least two columns"
        raise StopUpload(error_msg)

    table_meta = TableMetadata.objects.get(pk=table_id)
    table_meta.original_file_name = uploaded_file.name
    table_meta.save()

    for name in column_names:
        ColumnMetadata(
            table_metadata_id=table_id,
            name=name,
            title=name,
            description="",
            data_type_id=1,
            allow_missing_value=True,
            allow_duplicate_value=True,
        ).save()

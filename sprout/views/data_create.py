import csv

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.csv.csv_reader import read_csv_file
from sprout.models import ColumnMetadata, FileMetadata, TableMetadata
import os
from datetime import datetime
from sprout.uploaders import upload_raw_file


def data_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        uploaded_file = request.FILES.get("uploaded_file")
        file_path = upload_raw_file(uploaded_file)
        # Perform further processing or redirect to another page
        # Context?
        return HttpResponseRedirect("/next-page/")

    return render(request, "data-upload.html")


def project_id_data_id_metadata_create(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating metadata for data.

    The table_id comes from the url. The table_id is used fetch the
    table_metadata from the database.

    - On GET requests, the page is rendered.
    - On POST requests, the submitted CSV file is validated and column
      metadata persisted for the table.

    Args:
        request: the http request from the user/browser
        table_id: the table_id based

    Returns:
        HttpResponse: For GET requests and POST requests with errors
        HttpResponseRedirect: For POST request without any error
    """
    if request.method == "POST":
        return handle_post_request_with_file(request, table_id)

    return render_metadata_create_page(request, table_id, "")


def handle_post_request_with_file(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Validate CSV file in post request.

    The method have two scenarios:
    - If the validation is successful, then we persist the column metadata
      and redirect to the next page in the flow
    - If the validation fails, an exception is raised StopUpload. The page
      metadata-create page is re-rendered with the error message

    Args:
        request: http request from the user/browser
        table_id: the id of the table we are using

    Returns: A HttpResponseRedirect when validation is successful or
    HttpResponse when validation fails

    """
    file = request.FILES.get("uploaded_file", None)

    # To limit memory-usage we persist the file
    file_meta = FileMetadata.persist_raw_file(file, table_id)
    try:
        validate_csv_and_save_columns(table_id, file_meta)
    except csv.Error as csv_error:
        file_meta.delete()
        return render_metadata_create_page(request, table_id, csv_error.args[0])

    return redirect("/data/" + str(table_id) + "/metadata/edit/table")


def validate_csv_and_save_columns(table_id: int, file: FileMetadata) -> None:
    """Validate the csv and persist column metadata if valid.

    Args:
        table_id: The id of the table
        file: A file with a CSV file in files["uploaded_file"]
    """
    if file.file_extension != "csv":
        raise csv.Error("Unsupported file format: ." + file.file_extension)

    extract_and_persist_column_metadata(table_id, file)


def extract_and_persist_column_metadata(table_id: int, file: FileMetadata) -> None:
    """Extract columns from CSV and persist the column metadata.

    Args:
        table_id: The id of the table
        file: The CSV file
    """
    df = read_csv_file(file.server_file_path)

    # Save table
    table = TableMetadata.objects.get(pk=table_id)
    table.original_file_name = file.original_file_name
    table.save()

    # Save columns
    columns = [ColumnMetadata.create(table_id, series) for series in df]
    ColumnMetadata.objects.bulk_create(columns)

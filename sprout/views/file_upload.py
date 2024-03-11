"""File with metadata_create view."""

import csv

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.csv.csv_reader import read_csv_file
from sprout.models import ColumnMetadata, FileMetadata, TableMetadata


def metadata_create(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Method is called at url="metadata/create/<int:table_id>".

    The table_id comes from the url. The table_id is used fetch the
    table_metadata from the database.

    - On GET requests, the metadata/create page is rendered.
    - On POST requests, The submitted CSV file is validated and column
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
      file-upload page is re-rendered with the error message

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

    return redirect("/column-review/" + str(table_id))


def render_metadata_create_page(
    request: HttpRequest, table_id: int, upload_error: str
) -> HttpResponse:
    """Render metadata/create page with an error if there is any.

    Args:
        request: The http request
        table_id: The id of the table
        upload_error: The error message if there is any

    Returns:
        HttpResponse: A html page based on the file-upload.html template
    """
    table_metadata = TableMetadata.objects.get(pk=table_id)
    metadata_create_data = {
        "table_name": table_metadata.name,
        "upload_error": upload_error,
    }
    return render(request, "metadata-create.html", metadata_create_data)


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

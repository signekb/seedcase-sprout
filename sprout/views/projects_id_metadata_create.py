import csv

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.csv.csv_reader import read_csv_file
from sprout.models import Columns, Files, TableMetadata


def projects_id_metadata_create(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating metadata for data.

    The ``table_id`` comes from the URL. The ``table_id`` is used fetch the
    table_metadata from the database.

    - On GET requests, the page is rendered.
    - On POST requests, the submitted CSV file is validated and column
      metadata persisted for the table.

    Args:
        request: The HTTP request from the server.
        table_id: The ``table_id`` from the TableMetadata.

    Returns:
        HttpResponse: For GET requests and POST requests with errors
        HttpResponseRedirect: For POST request without any error
    """
    if request.method == "POST":
        return handle_post_request_with_file(request, table_id)

    return render_projects_id_metadata_create(request, table_id, "")


def handle_post_request_with_file(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Validate CSV file in post request.

    The method have two scenarios:
    - If the validation is successful, then we persist the column metadata
      and redirect to the next page in the flow
    - If the validation fails, an exception is raised StopUpload. The page
      is re-rendered with the error message

    Args:
        request: http request from the user/browser
        table_id: the id of the table we are using

    Returns: A HttpResponseRedirect when validation is successful or
    HttpResponse when validation fails

    """
    file = request.FILES.get("uploaded_file", None)

    # Delete exiting files, if user resubmits a file
    for previous_file in Files.objects.filter(table_metadata_id=table_id):
        previous_file.delete()

    # To limit memory-usage we persist the file
    file_meta = Files.create_model(file, table_id)
    try:
        validate_csv_and_save_columns(table_id, file_meta)
    except csv.Error as csv_error:
        file_meta.delete()
        return render_projects_id_metadata_create(request, table_id, csv_error.args[0])

    return redirect("/metadata/" + str(table_id) + "/update")


def render_projects_id_metadata_create(
    request: HttpRequest, table_id: int, upload_error: str
) -> HttpResponse:
    """Render page with an error if there is any.

    Args:
        request: The http request
        table_id: The id of the table
        upload_error: The error message if there is any

    Returns:
        HttpResponse: A html page based on the template
    """
    table_metadata = TableMetadata.objects.get(pk=table_id)
    context = {
        "table_name": table_metadata.name,
        "upload_error": upload_error,
    }
    return render(request, "projects-id-metadata-create.html", context)


def validate_csv_and_save_columns(table_id: int, file: Files) -> None:
    """Validate the csv and persist column metadata if valid.

    Args:
        table_id: The id of the table
        file: A file with a CSV file in files["uploaded_file"]
    """
    if file.file_extension != "csv":
        raise csv.Error("Unsupported file format: ." + file.file_extension)

    extract_and_persist_columns(table_id, file)


def extract_and_persist_columns(table_id: int, file: Files) -> None:
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

    # Delete columns if user resubmits csv file
    Columns.objects.filter(table_metadata_id=table.id).delete()

    # Save columns
    columns = [Columns.create(table_id, series) for series in df]
    Columns.objects.bulk_create(columns)

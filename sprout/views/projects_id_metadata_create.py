import csv
from typing import Dict, List

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from sprout.csv.csv_reader import read_csv_file
from sprout.forms import TablesForm, ColumnsForm
from sprout.models import Columns, Files, Tables


def projects_id_metadata_create(
    request: HttpRequest
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
    form_step_1 = TablesForm(data=None)
    table_id = -1
    columns = []

    if "table_id" in request.GET:
        table_id = int(request.GET["table_id"])
        table = Tables.objects.get(pk=table_id)
        form_step_1 = TablesForm(instance=table)
        columns = table.columns_set.all()

    if request.method == "POST":
        if not request.GET.get("step") or request.GET.get("step") == "1":
            form_step_1 = TablesForm(data=request.POST)
            if form_step_1.is_valid():
                table = form_step_1.save()

                qp = "?table_id=" + str(table.id) + "&step=2"
                url = reverse("projects-id-metadata-create") + qp
                return redirect(url)

        if request.GET.get("step") == "2":
            return handle_post_request_with_file(request, table_id)

        if request.GET.get("step") == "3":
            columns_metadata = Columns.objects.select_related("data_type").filter(
                tables=table)
            data_sample = create_sample_of_unique_values(table_id)
            forms = [create_form(request, c) for c in columns_metadata]
            columns = [
                {
                    "id": c.id,
                    "extracted_name": c.extracted_name,
                    "machine_readable_name": c.machine_readable_name,
                    "display_name": c.display_name,
                    "description": c.description,
                    "data_type": c.data_type.display_name,
                    "data": data_sample[c.extracted_name],
                    "form": forms[idx],
                }
                for idx, c in enumerate(columns_metadata)
            ]

            # if request.method == "POST":
            #     for form in forms:
            #         if form.is_valid():
            #             form.save()
            #
            #         # Delete excluded columns
            #         if form.cleaned_data["excluded"]:
            #             form.instance.delete()
            #
            #     qp = "?table_id=" + str(table.id) + "&step=4"
            #     url = reverse("projects-id-metadata-create") + qp
            #     return redirect(url)

            return render(
                request,
                "projects-id-metadata-create.html",
                {
                    "forms": forms,
                    "tables": table,
                    "columns": columns,
                },
            )


    context = {
        "form_step_1": form_step_1,
        "columns": columns,
    }
    return render(request, "projects-id-metadata-create.html", context)


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
    for previous_file in Files.objects.filter(tables_id=table_id):
        previous_file.delete()

    # To limit memory-usage we persist the file
    file_meta = Files.create_model(file, table_id)
    try:
        validate_csv_and_save_columns(table_id, file_meta)
    except csv.Error as csv_error:
        file_meta.delete()
        return render_projects_id_metadata_create(request, table_id, csv_error.args[0])

    qp = "?table_id=" + str(table_id) + "&step=3"
    url = reverse("projects-id-metadata-create") + qp
    return redirect(url)


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
    tables = Tables.objects.get(pk=table_id)
    context = {
        "table_name": tables.name,
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
    table = Tables.objects.get(pk=table_id)
    table.original_file_name = file.original_file_name
    table.save()

    # Delete columns if user resubmits csv file
    Columns.objects.filter(tables_id=table.id).delete()

    # Save columns
    columns = [Columns.create(table_id, series) for series in df]
    Columns.objects.bulk_create(columns)

def create_form(request: HttpRequest, column: Columns) -> ColumnsForm:
    """Create form based on request can Columns.

    Args:
        request: The HttpRequest sent.
        column: Django model data from Columns.

    Returns:
        Outputs the ColumnsForm Django model object.
    """
    if request.method == "POST":
        return ColumnsForm(request.POST, instance=column, prefix=str(column.id))
    else:
        return ColumnsForm(instance=column, prefix=str(column.id))


def create_sample_of_unique_values(tables_id: int) -> Dict[str, List]:
    """Create sample of unique values based on the uploaded file for a table.

    The unique values are based on the first 500 rows.

    Args:
        tables_id: The id of the table

    Returns:
        Dict[str, List]: Dictionary of unique sample values grouped by column name.
    """
    file = Files.objects.get(tables_id=tables_id)
    df = read_csv_file(file.server_file_path, 500)

    # Find unique values, and limit to max 5 different
    return dict(
        [(s.name, s.unique(maintain_order=True).limit(5).to_list()) for s in df]
    )

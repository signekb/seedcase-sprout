"""File with column_review view."""

from typing import Dict, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from sprout.csv.csv_reader import read_csv_file
from sprout.forms import ColumnsForm
from sprout.models import Columns, Files, Tables
from sprout.views.projects_id_metadata_id.helpers import create_stepper_url


def step_columns(request: HttpRequest, table_id: int) -> HttpResponse:
    """Renders the step with metadata columns."""
    tables = get_object_or_404(Tables, id=table_id)
    columns_metadata = Columns.objects.select_related("data_type").filter(tables=tables)
    data_sample = create_sample_of_unique_values(tables.id)
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

    if request.method == "POST":
        for form in forms:
            if form.is_valid():
                form.save()

            # Delete excluded columns
            if form.cleaned_data["excluded"]:
                form.instance.delete()

        return redirect(create_stepper_url(4, table_id))

    return render(
        request,
        "projects-id-metadata-create.html",
        {
            "forms": forms,
            "tables": tables,
            "columns": columns,
        },
    )


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

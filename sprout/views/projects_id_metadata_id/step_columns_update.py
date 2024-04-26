"""File with column_review view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from sprout.models import Columns, Tables
from sprout.views.projects_id_metadata_id.helpers import create_stepper_url
from sprout.views.projects_id_metadata_id_update import (
    create_form,
    create_sample_of_unique_values,
)


def step_columns_update(request: HttpRequest, table_id: int) -> HttpResponse:
    """Takes the data from Columns and displays the metadata to update."""
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
        "projects_id_metadata_id/create.html",
        {
            "forms": forms,
            "tables": tables,
            "columns": columns,
        },
    )

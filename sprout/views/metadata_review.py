from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from sprout.csv.csv_reader import read_csv_file
from sprout.forms import ColumnMetadataForm
from sprout.models import ColumnMetadata, FileMetadata, TableMetadata


def metadata_review(request: HttpRequest, table_id: int):
    """Review and edit column metadata."""
    table_metadata = get_object_or_404(TableMetadata, id=table_id)
    columns_metadata = ColumnMetadata.objects.select_related("data_type").filter(
        table_metadata=table_metadata
    )
    file = FileMetadata.objects.get(table_metadata=table_metadata)
    df = read_csv_file(file.server_file_path, 5)
    forms = [create_form(request, c) for c in columns_metadata]

    columns = [
        {
            "original_name": c.original_name,
            "title": c.title,
            "name": c.name,
            "description": c.description,
            "data_type": c.data_type.display_name,
            "data": df[c.original_name].to_list(),
            "tab-index": idx,
            "form": forms[idx],
        }
        for idx, c in enumerate(columns_metadata)
    ]

    if request.method == "POST" and all(f.is_valid() for f in forms):
        for form in forms:
            form.save()
        return redirect(reverse("metadata-review", args=[table_id]))

    return render(
        request,
        "metadata-review.html",
        {
            "table_metadata": table_metadata,
            "columns": columns,
        },
    )


def create_form(request: HttpRequest, column: ColumnMetadata) -> ColumnMetadataForm:
    """Create form based on request can ColumnMetadata."""
    if request.method == "POST":
        return ColumnMetadataForm(request.POST, instance=column, prefix=str(column.id))
    else:
        return ColumnMetadataForm(instance=column, prefix=str(column.id))

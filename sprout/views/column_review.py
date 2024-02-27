"""File with column_review view."""

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from sprout.forms import ColumnMetadataForm
from sprout.models import ColumnMetadata, TableMetadata


def column_review(request, table_id):
    """Takes the data from ColumnMetadata and displays as a table.

    The table can be edited and the result written back to the db

    Args: Must learn what to write here
        request (_type_): _description_
        table_name (_type_): _description_

    Returns: Must learn what to write here
        _type_: _description_
    """
    table_metadata = get_object_or_404(TableMetadata, id=table_id)
    columns_metadata = ColumnMetadata.objects.filter(table_metadata=table_metadata)

    if request.method == "POST":
        forms = [
            ColumnMetadataForm(request.POST, instance=column, prefix=str(column.id))
            for column in columns_metadata
        ]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect(reverse("column-review", args=[table_id]))
        else:
            print([form.errors for form in forms])
    else:
        forms = [
            ColumnMetadataForm(instance=column, prefix=str(column.id))
            for column in columns_metadata
        ]

    return render(
        request,
        "column-review.html",
        {
            "forms": forms,
            "table_metadata": table_metadata,
            "columns_metadata": columns_metadata,
        },
    )

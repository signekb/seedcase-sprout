from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from app.forms import ColumnDataTypeForm, ColumnMetadataForm
from app.models import ColumnDataType, ColumnMetadata, TableMetadata


# def column_review(request):
#     # Retrieve data with join using select_related
#     columns_data = ColumnMetadata.objects.select_related(
#         "data_type", "table_metadata"
#     ).all()
#     return render(request, "column-review.html", {"cols": columns_data})


def column_review(request):
    ColumnTypeFormSet = modelformset_factory(
        ColumnMetadata, form=ColumnMetadataForm
    )
    formset = ColumnTypeFormSet(queryset=ColumnMetadata.objects.all())

    return render(
        request,
        "column-review.html",
        {"formset": formset},
    )


def columndata_review(request):
    ColumnDataTypeFormSet = modelformset_factory(
        ColumnDataType, form=ColumnDataTypeForm
    )
    formset = ColumnDataTypeFormSet(queryset=ColumnDataType.objects.all())

    return render(
        request,
        "columndata-review.html",
        {"formset": formset},
    )


def update_columns_for_table(request, table_name):
    table_metadata = get_object_or_404(TableMetadata, name=table_name)
    columns_metadata = ColumnMetadata.objects.filter(
        table_metadata=table_metadata
    )

    if request.method == "POST":
        forms = [
            ColumnMetadataForm(request.POST, instance=column)
            for column in columns_metadata
        ]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect("home")  # Redirect to a success page
        # else:
        #     print([form.errors for form in forms])
    else:
        forms = [
            ColumnMetadataForm(instance=column) for column in columns_metadata
        ]

    return render(
        request,
        "update-columns-for-table.html",
        {
            "forms": forms,
            "table_metadata": table_metadata,
            "columns_metadata": columns_metadata,
        },
    )

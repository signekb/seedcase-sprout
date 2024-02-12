from django.shortcuts import render  # , redirect

from app.models import ColumnMetadata, ColumnDataType, TableMetadata
from app.forms import ColumnDataTypeForm
from django.forms import modelformset_factory


def column_review(request):
    # Retrieve data with join using select_related
    columns_data = ColumnMetadata.objects.select_related(
        "data_type", "table_metadata"
    ).all()
    return render(request, "column-review.html", {"cols": columns_data})


# def columndata_review(request):
#     data = ColumnDataType.objects.all()
#     ColumnDataTypeformSet = ColumnDataTypeForm(queryset=data)
#     return render(
#         request,
#         "columndata-review.html",
#         {"ColumnDataTypeFormSet": ColumnDataTypeformSet},
#     )
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

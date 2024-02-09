from django.shortcuts import render #, redirect

from app.models import ColumnMetadata, ColumnDataType, TableMetadata

def column_review(request):
  # Retrieve data with join using select_related
  columns_data = ColumnMetadata.objects.select_related('data_type', 'table_metadata').all()
  return render(request, 'column-review.html', {'cols':columns_data})

def columndata_review(request):
  colsdata = ColumnDataType.objects
  return render(request, 'columndata-review.html', {'colsdata':colsdata})
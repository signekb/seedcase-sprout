from django.shortcuts import render #, redirect

from app.models import ColumnMetadata, ColumnDataType

def column_review(request):
  cols = ColumnMetadata.objects
  return render(request, 'column-review.html', {'cols':cols})

def columndata_review(request):
  colsd = ColumnDataType.objects
  return render(request, 'columndata-review.html', {'colsdata':colsd})

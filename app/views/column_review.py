from django.shortcuts import render #, redirect

from app.models import ColumnMetadata

def column_view(request):
  #cols = ColumnMetadata.objects
  return render(request, 'column-review.html')
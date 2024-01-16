from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from app.models import TableMetadata, ColumnMetadata, ColumnDataType


def index(request):
    tables = TableMetadata.objects.all()
    print('Table row count before', tables.count())

    t = TableMetadata(name="Tabel1", original_file_name="my.csv", description="First table", created_by=1)
    t.save()

    dt = ColumnDataType(display_name="Text")
    dt.save()

    c = ColumnMetadata(table_metadata=t, name="CPR", title="CPR", description="id", data_type=dt, allow_missing_value=True, allow_duplicate_value=True)
    c.save()

    print('Table row count after', tables.count())
    return HttpResponse("Hello go to /hello to render a template")


def hello_world(request):
    now = datetime.now()
    return render(request, "hello.html", {"now": now})

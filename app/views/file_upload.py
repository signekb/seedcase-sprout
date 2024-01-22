from django.shortcuts import render, redirect

from app.models import ColumnMetadata, TableMetadata


def extract_and_persist_column_metadata(table_id, uploaded_file):
    # A more complicated function needs to be added
    column_names = uploaded_file.readline().decode("utf-8").split(",")
    for name in column_names:
        ColumnMetadata(
            table_metadata_id=table_id,
            name=name,
            title=name,
            description="",
            data_type_id=1,
            allow_missing_value=True,
            allow_duplicate_value=True
        ).save()


def file_upload(request, table_id):
    table_metadata = TableMetadata.objects.get(pk=table_id)
    file_upload_data = {'table_name': table_metadata.name, 'upload_error': ''}
    if request.method == 'GET':
        return render(request, "file-upload.html", file_upload_data)

    # File is missing
    if 'uploaded_file' not in request.FILES:
        file_upload_data["upload_error"] = "MissingFile"
        return render(request, "file-upload.html", file_upload_data)

    uploaded_file = request.FILES["uploaded_file"]
    extract_and_persist_column_metadata(table_id, uploaded_file)
    return redirect("/edit-table-columns/" + str(table_id))

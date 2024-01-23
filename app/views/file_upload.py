from django.shortcuts import render, redirect

from app.models import ColumnMetadata, TableMetadata


def file_upload(request, table_id):
    if request.method == "GET":
        return render_file_upload_page(request, table_id, "")

    upload_error = extract_columns_and_get_error(table_id, request.FILES)
    if upload_error:
        return render_file_upload_page(request, table_id, upload_error)

    return redirect("/edit-table-columns/" + str(table_id))


def render_file_upload_page(request, table_id, upload_error):
    table_metadata = TableMetadata.objects.get(pk=table_id)
    file_upload_data = {"table_name": table_metadata.name, "upload_error": upload_error}
    return render(request, "file-upload.html", file_upload_data)


def extract_columns_and_get_error(table_id, files):
    # File is missing
    uploaded_file = files.get("uploaded_file", None)
    if not uploaded_file:
        return "The file is missing!"

    if not uploaded_file.name.endswith(".csv"):
        return "Unsupported file format: ." + uploaded_file.name.split(".")[-1]

    return extract_and_persist_column_metadata(table_id, uploaded_file)


def extract_and_persist_column_metadata(table_id, uploaded_file):
    # A more complicated function needs to be added
    column_names = uploaded_file.readline().decode("utf-8").split(",")

    if len(column_names) < 2:
        return "Unable to extract column headers"

    for name in column_names:
        ColumnMetadata(
            table_metadata_id=table_id,
            name=name,
            title=name,
            description="",
            data_type_id=1,
            allow_missing_value=True,
            allow_duplicate_value=True,
        ).save()
    return ""

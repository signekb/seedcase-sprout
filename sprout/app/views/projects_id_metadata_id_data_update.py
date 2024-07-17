import polars as pl
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from sprout.app.models import Columns, Files, Tables


def projects_id_metadata_id_data_update(
    request: HttpRequest, table_id: int
) -> HttpResponse:
    """Modifies or adds data in a database table for a specific metadata object.

    Args:
        request: Takes the HTTP request from the server.
        table_id: The database Table ID.

    Returns:
        Outputs an HTTP response object.
    """
    table = get_object_or_404(Tables, id=table_id)
    context = {
        "upload_success": False,
        "table_name": table.name,
    }
    if request.method == "POST":
        new_uploaded_file = get_uploaded_file(request)
        files = Files.create_model(new_uploaded_file, table_id)
        new_server_file = files.server_file_path
        # schema = get_schema(id=table_id)
        # data_update = read_csv_file(new_server_file, row_count=None)

        # TODO: Implement these below later
        # Inform if there are columns that exist in the uploaded data,
        # that don't exist in the schema
        # verify_headers(data, schema)
        # verify_data_types(data, schema)
        #   if false delete uploaded file (inside functions?)

        # TODO: We need to set up the database first, which I don't know how to do yet
        # data_current = read_database(path=Paths.database, table_name=table_id)
        # data_updated = data_current.join(other=data_update)  # from polars
        # data_updated.write_database(
        #     table_name=table_metadata.name,
        #     connection=Paths.database,
        #     # TODO: There is also append, but not sure we want to append rather than
        #     # join by ID in the table.
        #     if_table_exists="replace",
        #     # TODO: Not sure which engine to use. Alternative is "adbc"
        #     # engine="sqlalchemy"
        # )
        # TODO: verify that database has been written to.

        # update tables model with new data rows
        new_rows_added = count_rows(new_server_file)
        table.data_rows = table.data_rows + new_rows_added
        table.save()

        context = {
            "table_name": table.name,
            "upload_success": True,
            "file_metadata": files,
            "number_rows": new_rows_added,
        }

    # TODO: Provide context for response instead of redirect?
    # And button in template to move to other page?
    return render(request, "projects-id-metadata-id-data-update.html", context)


class Paths:
    """List of paths used throughout Sprout."""

    # TODO: Not sure how this will look like.
    database = "PATH"


def read_database(path: str, table_name: str) -> pl.DataFrame:
    """Read a specific table from the database."""
    # TODO: Don't know how the connection will look like with Postgres
    return pl.read_database(query=f"SELECT * FROM {table_name}", connection=path)


def get_uploaded_file(request: HttpRequest) -> UploadedFile:
    """Get uploaded file name from the HTTP request."""
    return request.FILES.get("uploaded_file")


def count_rows(path: str) -> int:
    """Count the number of rows in a file."""
    # TODO: This might not always be a csv.
    data = pl.scan_csv(path)
    return data.select(pl.len()).collect().item()


def get_schema(id: int) -> Columns:
    """Get the schema of a specific table via Columns model."""
    return Columns.objects.get(id=id)

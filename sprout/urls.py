"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path(
        "metadata/<int:table_id>/data/update",
        views.project_id_metadata_id_data_update,
        name="project-id-metadata-id-data-update",
    ),
    path(
        "metadata/create/<int:table_id>", views.metadata_create, name="metadata-create"
    ),
    path(
        "column-review/<int:table_id>",
        views.column_review,
        name="column-review",
    ),
    path("table-files/<int:table_id>", views.table_files, name="table-files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table-file-download",
    ),
]

"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path(
        "data/<int:table_id>/upload",
        views.project_id_data_id_upload,
        name="project-id-data-id-upload",
    ),
    path(
        "metadata/create/<int:table_id>",
        views.metadata_create,
        name="metadata-create",
    ),
    path(
        "column-review/<int:table_id>",
        views.column_review,
        name="column-review",
    ),
    path(
        "project-id-metadata-view",
        views.project_id_metadata_view,
        name="project-id-metadata-view",
    ),
    path(
        "table-files/<int:table_id>",
        views.table_files,
        name="table-files",
    ),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table-file-download",
    ),
]

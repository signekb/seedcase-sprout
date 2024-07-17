"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.projects_id_metadata_view, name="projects-id-metadata-view"),
    path(
        "metadata/<int:table_id>/data/update",
        views.projects_id_metadata_id_data_update,
        name="projects-id-metadata-id-data-update",
    ),
    path("view", views.projects_id_view, name="projects-id-view"),
    path(
        "metadata/create",
        views.projects_id_metadata_create,
        name="projects-id-metadata-create",
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

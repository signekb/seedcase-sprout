"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view", views.projects_id_view, name="projects-id-view"),
    path(
        "data/<int:table_id>/metadata/create", views.projects_id_data_id_metadata_create
    ),
    path(
        "data/<int:table_id>/metadata/edit/table",
        views.projects_id_data_id_metadata_edit_table,
        name="projects-id-data-id-metadata-edit-table",
    ),
    path(
        "data/<int:table_id>/metadata/edit/grid",
        views.projects_id_data_id_metadata_edit_grid,
        name="projects-id-data-id-metadata-edit-grid",
    ),
    path("table-files/<int:table_id>", views.table_files, name="table_files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table_file_download",
    ),
]

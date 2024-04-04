"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view", views.projects_id_view, name="projects-id-view"),
    path(
        "metadata/<int:table_id>/create",
        views.projects_id_metadata_create,
        name="projects-id-metadata-create",
    ),
    path(
        "metadata/<int:table_id>/update",
        views.projects_id_metadata_id_update,
        name="projects-id-metadata-id-update",
    ),
    path(
        "project-id-metadata-view",
        views.project_id_metadata_view,
        name="project-id-metadata-view",
    ),
    path("table-files/<int:table_id>", views.table_files, name="table-files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table-file-download",
    ),
]

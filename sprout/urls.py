"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view", views.project_id_view, name="project-id-view"),
    path("metadata/create/<int:table_id>", views.metadata_create),
    path(
        "column-review/<int:table_id>",
        views.column_review,
        name="column-review",
    ),
    path(
        "data/<int:table_id>/metadata/edit/grid",
        views.column_review_list,
        name="project-id-data-id-metadata-edit-grid",
    ),
    path("table-files/<int:table_id>", views.table_files, name="table_files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table_file_download",
    ),
]

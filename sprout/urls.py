"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path("upload", views.upload_csv, name="upload_csv"),
    path("metadata/create/<int:table_id>", views.metadata_create),
    path(
        "column-review/<int:table_id>/",
        views.column_review,
        name="column-review",
    ),
    path("table-files/<int:table_id>", views.table_files, name="table_files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table_file_download",
    ),
]

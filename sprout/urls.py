"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path("file-upload/<int:table_id>", views.file_upload),
    path("table-files/<int:table_id>", views.table_files, name="table_files"),
    path(
        "table-files/<int:table_id>/download/<int:file_id>",
        views.table_file_download,
        name="table_file_download",
    ),
]

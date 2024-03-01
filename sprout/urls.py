"""Sprout URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path("file-upload/<int:table_id>", views.file_upload),
    path("upload", views.upload_csv, name="upload_csv"),
]

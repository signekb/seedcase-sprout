"""App URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path("file-upload/<int:table_id>", views.file_upload),
    path(
        "columndata-review", views.columndata_review, name="columndata-review"
    ),
    path(
        "column-review/<str:table_name>/",
        views.column_review,
        name="column-review",
    ),
]

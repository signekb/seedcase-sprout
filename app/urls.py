from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data-import", views.data_import, name="data_import"),
    path("file-upload/<int:table_id>", views.file_upload),
    path("column-review", views.column_review, name="column-review"),
    path(
        "columndata-review", views.columndata_review, name="columndata-review"
    ),
    path(
        "update-columns-for-table/<str:table_name>/",
        views.update_columns_for_table,
        name="update-columns-for-table",
    ),
]

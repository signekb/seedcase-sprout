"""Module with all views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .projects_id_metadata_create import projects_id_metadata_create
from .projects_id_metadata_id_data_update import projects_id_metadata_id_data_update
from .projects_id_metadata_id_update import projects_id_metadata_id_update
from .projects_id_metadata_view import projects_id_metadata_view
from .projects_id_view import projects_id_view
from .table_files import table_file_download, table_files

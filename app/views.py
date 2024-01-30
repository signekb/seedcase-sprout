from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from app.forms import TableMetadataForm


def home(request):
    return render(request, "home.html")


def data_import(request):
    # if this is a POST request, process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(request.POST)

        # if user input passes validation, save form and redirect to file upload
        if form.is_valid():

            return redirect(to=f"file-upload/{table_metadata.id}")

    # if GET (or any other method), create a blank form
    else:
        form = TableMetadataForm()

    return render(request, "data-import.html", {"form": form})

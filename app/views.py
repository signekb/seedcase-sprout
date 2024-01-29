from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.forms import TableMetadataForm


def home(request):
    return render(request, "home.html")


def data_import(request):
    # if this is a POST request, we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(request.POST)

        # if user input passes validation
        if form.is_valid():

            table = form.save()

            return HttpResponseRedirect(f"/file-upload/{table.id}")

    # if GET (or any other method) we'll create a blank form
    else:
        form = TableMetadataForm()

    return render(request, "data-import.html", {"form": form})

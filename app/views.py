from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.forms import TableMetadataForm
from app.validators.model_dependent_validators import does_table_name_exist_in_db


def home(request):
    return render(request, "home.html")


def data_import(request):
    # if this is a POST request, we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(request.POST)

        # if user input passes validation
        if form.is_valid():
            # extra val: does table name exist in db
            name = form.cleaned_data["name"]

            if does_table_name_exist_in_db(name=name):
                return render(
                    request,
                    "data-import.html",
                    {
                        "form": form,
                        "error_msg": "Table name already exists. Please provide another name.",
                    },
                )

            table = form.save()

            return HttpResponseRedirect(f"/file-upload/{table.id}")

    # if GET (or any other method) we'll create a blank form
    else:
        form = TableMetadataForm()

    return render(request, "data-import.html", {"form": form})

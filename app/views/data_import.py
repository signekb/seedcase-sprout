from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from app.forms import TableMetadataForm


def data_import(request: HttpRequest) -> HttpResponse:
    """data_import Import data from form.

    Initially renders a blank form using the ``data-import`` template, if
    ``request.method != "POST"``.  If ``request.method == "POST"``, the form is
    validated.  If validation is successful, the form is saved and the page is
    redirected to the ``file-upload`` template.

    Args:
        request (HttpRequest): Contains metadata about the request, including
        method ("POST", "GET") and input in the form.

    Returns:
        HttpResponse:
            If ``request.method != "POST"``, a ``HttpResponse`` is returned (using the Django shortcut render).
            If ``request.method == "POST"`` and validation is successful, a ``HttpResponseRedirect`` is returned.
    """
    # if this is a POST request, process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TableMetadataForm(data=request.POST)

        # if user input passes validation, save form and redirect to file upload
        if form.is_valid():
            table_metadata = form.save()

            return redirect(to=f"file-upload/{table_metadata.id}")

    # if GET (or any other method), create a blank form
    else:
        form = TableMetadataForm(data=None)

    return render(
        request=request,
        template_name="data-import.html",
        context={"form": form},
    )

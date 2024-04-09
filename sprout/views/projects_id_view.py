"""File with data_import view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sprout.forms import TablesForm


def projects_id_view(request: HttpRequest) -> HttpResponse:
    """Landing page for the project.

    Initially renders a blank form using the template, if
    ``request.method != "POST"``.  If ``request.method == "POST"``, the form is
    validated.  If validation is successful, the form is saved and the page is
    redirected to the correct template.

    Args:
        request (HttpRequest): Contains metadata about the request, including method
            ("POST", "GET") and input in the form.

    Returns:
        HttpResponse:
            If ``request.method != "POST"``, a ``HttpResponse`` is returned
                (using theDjango shortcut render).
            If ``request.method == "POST"`` and validation is successful,
                a ``HttpResponseRedirect`` is returned.
    """
    # if this is a POST request, process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = TablesForm(data=request.POST)

        # if input passes validation, save form and redirect to file upload
        if form.is_valid():
            tables = form.save()
            return redirect(
                to=reverse(
                    "projects-id-metadata-create",
                    kwargs={"table_id": tables.id},
                )
            )

    # if GET (or any other method), create a blank form
    else:
        form = TablesForm(data=None)

    return render(
        request=request,
        template_name="projects-id-view.html",
        context={"form": form},
    )

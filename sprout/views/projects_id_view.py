"""File with data_import view."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from sprout.forms import TableMetadataForm


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
        form = TableMetadataForm(data=request.POST)

        # if input passes validation, save form and redirect to file upload
        if form.is_valid():
            table_metadata = form.save()

            return redirect(to=f"data/{table_metadata.id}/metadata/create")

    # if GET (or any other method), create a blank form
    else:
        form = TableMetadataForm(data=None)

    return render(
        request=request,
        template_name="projects-id-view.html",
        context={"form": form},
    )

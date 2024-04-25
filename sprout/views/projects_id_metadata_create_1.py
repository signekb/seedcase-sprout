from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.forms import TablesForm
from sprout.views.projects_id_metadata_create_helper import create_stepper_url


def projects_id_metadata_create_1(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating name and description for metadata."""
    form_step_1 = TablesForm(data=None)

    if request.method == "POST":
        form_step_1 = TablesForm(data=request.POST)
        if form_step_1.is_valid():
            form_step_1.instance.id = table_id
            table = form_step_1.save()

            return redirect(create_stepper_url(2, table.id))

    context = {
        "form_step_1": form_step_1,
    }
    return render(request, "projects-id-metadata-create.html", context)

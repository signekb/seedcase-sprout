from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.forms import TablesForm
from sprout.views.projects_id_metadata_id.helpers import create_stepper_url


def step_name_and_description(
    request: HttpRequest, table_id: int | None
) -> HttpResponse | HttpResponseRedirect:
    """Renders page for creating name and description for metadata."""
    form = TablesForm(data=None)

    if request.method == "POST":
        form = TablesForm(data=request.POST)
        if form.is_valid():
            form.instance.id = table_id
            table = form.save()

            return redirect(create_stepper_url(2, table.id))

    context = {
        "form": form,
    }
    return render(request, "projects_id_metadata_id/create.html", context)

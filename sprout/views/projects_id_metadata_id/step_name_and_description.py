from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from sprout.forms import TablesForm
from sprout.models import Tables
from sprout.views.projects_id_metadata_id.helpers import create_stepper_url


def step_name_and_description(
    request: HttpRequest, table_id: int | None
) -> HttpResponse | HttpResponseRedirect:
    """Renders step creating/editing metadata name and description."""
    form = TablesForm(data=None)
    table = None
    if table_id:
        table = Tables.objects.get(pk=table_id)
        form = TablesForm(instance=table)

    if request.method == "POST":
        form = TablesForm(data=request.POST)
        if table:
            form = TablesForm(data=request.POST, instance=table)

        if form.is_valid():
            table = form.save()
            return redirect(create_stepper_url(2, table.id))

    context = {
        "form": form,
    }
    return render(request, "projects-id-metadata-create.html", context)

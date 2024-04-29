from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from sprout.models import Tables


def step_confirmation(
    request: HttpRequest, table_id: int
) -> HttpResponse | HttpResponseRedirect:
    """Renders the final confirmation step when creating/updating metadata."""
    table = Tables.objects.prefetch_related("columns_set").get(pk=table_id)
    if request.method == "POST":
        table = Tables.objects.get(pk=table_id)
        table.is_draft = False
        table.save()
        return redirect(reverse("projects-id-metadata-view"))
    context = {"table": table}
    return render(request, "projects-id-metadata-create.html", context)

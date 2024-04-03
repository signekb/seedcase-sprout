"""Views for the accounts app."""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import RegisterForm
from accounts.models import CustomUser


def accounts_register(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Renders account registration page.

    Args:
        request: A http request from the client

    Returns:
        HttpResponseRedirect: When account is registered successfully
        HttpResponse: The registration page is rendered on GET requests and when
                      validation fails.
    """
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            CustomUser.objects.create_user(username, email, password)
            return redirect(reverse("login"))

    return render(request, "registration/register.html", {"form": form})

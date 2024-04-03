from django.urls import include, path

from accounts.views import accounts_register

urlpatterns = [
    # Django provides default urls and views for handling login, password_reset and
    # password_change. Read more here:
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#using-the-views
    path("", include("django.contrib.auth.urls")),

    # A view for registering a user (this is not provided by Django)
    path("register", accounts_register, name="register"),
]

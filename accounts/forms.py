"""Forms for accounts app."""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """UserCreationForm is extended with email.

    Email should be used instead of just username, so UserCreationForm is extended
    with email.
    """

    class Meta:
        """Meta is required on derived class."""

        model = get_user_model()
        fields = ("email", "username", "password1", "password2")

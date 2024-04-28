from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class AuthenticationTests(TestCase):
    """Testing authentication flows."""

    valid_mail = "philter@philter.com"
    username = "PhilterMachine"

    def test_valid_account_registration(self):
        """Register account with valid credentials."""
        # Arrange
        url = reverse("register")
        form_data = {
            "username": self.username,
            "email": self.valid_mail,
            "password1": "as123dsSf",
            "password2": "as123dsSf",
        }

        # Act
        response = self.client.post(url, form_data)

        # Assert
        user = CustomUser.objects.first()
        self.assertEqual(self.username, user.username)
        self.assertEqual(self.valid_mail, user.email)
        self.assertRedirects(
            response, reverse("login"), status_code=302, target_status_code=200
        )

    def test_invalid_account_registration(self):
        """Registering account fails because of insecure password."""
        # Arrange
        url = reverse("register")
        form_data = {
            "username": self.username,
            "email": self.valid_mail,
            "password1": "123456",
            "password2": "123456",
        }

        # Act
        response = self.client.post(url, form_data)

        # Assert
        self.assertContains(response, "This password is too short")
        self.assertContains(response, "This password is too common")
        self.assertContains(response, "This password is entirely numeric")

    def test_create_account_and_login(self):
        """Register and login with account."""
        # Arrange
        password = "as123dsSf"

        register_form = {
            "username": self.username,
            "email": self.valid_mail,
            "password1": password,
            "password2": password,
        }
        login_form = {"username": self.valid_mail, "password": password}

        # Act
        self.client.post(reverse("register"), register_form)
        response = self.client.post(reverse("login"), login_form)

        # Assert
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

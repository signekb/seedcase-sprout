"""Configuration module for "sprout"."""
import sys

from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate

from config.settings import DEBUG


class AppConfig(AppConfig):
    """The configuration for "sprout"."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sprout"

    def ready(self) -> None:
        """This is executed when the app starts up."""
        # We do a lazy import, otherwise the app will fail with
        # AppRegistryNotReady
        from sprout.models.column_data_type import update_column_data_types

        # We use a Django signal called post_migrate as the columns should
        # update after the migrations have been applied.
        post_migrate.connect(update_column_data_types, sender=self)

        # Adding test data after migrate when DEBUG=TRUE and not running unit tests
        is_running_unit_tests = 'test' not in sys.argv
        if DEBUG and is_running_unit_tests:
            post_migrate.connect(load_test_data, sender=self)


def load_test_data(**kwargs):
    """Loads test data in 'patients.json'.

    You can create new test data with:
    'python manage.py dumpdata | file_name.json'
    """
    print("TEST DATA IS LOADED")
    call_command('loaddata', 'patients')

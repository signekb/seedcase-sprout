from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self) -> None:
        """This is executed when the app starts up."""
        # We do a lazy import, otherwise the app will fail with
        # AppRegistryNotReady
        from app.models.column_data_type import update_column_data_types

        # We use a Django signal called post_migrate as the columns should
        # update after the migrations have been applied.
        post_migrate.connect(update_column_data_types, sender=self)

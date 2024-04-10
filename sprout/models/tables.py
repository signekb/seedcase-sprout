"""Module defining the Tables model."""

from datetime import datetime, timezone

from django.conf import settings
from django.db import models


class Tables(models.Model):
    """Model representing the table metadata."""

    name = models.CharField(max_length=128)
    original_file_name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.PROTECT,
        related_name="creator",
    )
    modified_at = models.DateTimeField(null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.PROTECT,
        related_name="modifier",
    )
    data_rows = models.IntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        """Overriding the default save-method.

        modified_at should only change when modified and not when created.
        
        Args:
            *args: non-keyword arguments required by Django
            **kwargs: keyword arguments required by Django.
        """
        if self.id:
            self.modified_at = datetime.now(timezone.utc)

        super().save(*args, **kwargs)

"""Model for a persisted file."""

import os
import uuid
from typing import IO

from django.conf import settings
from django.db import models

from sprout.app.models.tables import Tables
from sprout.app.uploaders import write_to_raw


class Files(models.Model):
    """Model for a persisted file."""

    original_file_name = models.TextField()
    server_file_path = models.TextField()
    file_extension = models.CharField(max_length=10)
    file_size_bytes = models.BigIntegerField()

    tables = models.ForeignKey(Tables, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT
    )
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_model(file: IO, tables_id: int) -> "Files":
        """Persists a file and stores metadata in database.

        Args:
            file: The file to persist
            tables_id: The id of the table

        Returns:
            Files: The relative path on the server
        """
        file_extension = file.name.split(".")[-1]
        file_name_wo_ext = file.name.split(".")[-2][:150]
        unique_file_name = f"{file_name_wo_ext}-{uuid.uuid4().hex}.{file_extension}"

        server_file_path = write_to_raw(file, unique_file_name)

        files = Files.objects.create(
            original_file_name=file.name,
            server_file_path=server_file_path,
            file_size_bytes=os.path.getsize(server_file_path),
            file_extension=file_extension,
            tables_id=tables_id,
        )

        return files

    def delete(self, *args, **kwargs) -> None:
        """Overriding the default delete method as the file should be deleted as well.

        We want to delete the actual file, when the metadata for a file is deleted. We
        can do this by overriding the default delete method and adding som extra
        behaviour.

        NOTICE: This is NOT called on a QuerySet: Files.objects.delete()

        Args:
            *args: The positional arguments required by Django
            **kwargs: The keyword arguments required by Django
        """
        # The normal delete logic is called:
        super().delete(*args, **kwargs)

        # And we delete the file
        os.remove(self.server_file_path)

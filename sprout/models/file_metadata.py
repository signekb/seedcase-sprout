"""Model for a persisted file."""

import os
import uuid
from typing import IO

from django.conf import settings
from django.db import models

from config.settings import PERSISTENT_STORAGE_PATH
from sprout.models.table_metadata import TableMetadata
from sprout.uploaders import upload_raw_file


class FileMetadata(models.Model):
    """Model for a persisted file."""

    original_file_name = models.TextField()
    server_file_path = models.TextField()
    file_extension = models.CharField(max_length=10)
    file_size_bytes = models.BigIntegerField()

    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT
    )
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def persist_raw_file(file: IO, table_metadata_id: int) -> "FileMetadata":
        """Persists a file and stores metadata in database.

        Args:
            file: The file to persist
            table_metadata_id: The id of the table

        Returns:
            FileMetadata: The relative path on the server
        """
        file_extension = file.name.split(".")[-1]
        file_name_wo_ext = file.name.split(".")[-2][:150]
        unique_file_name = f"{file_name_wo_ext}-{uuid.uuid4().hex}.{file_extension}"

        server_file_path = upload_raw_file(file, unique_file_name)

        file_metadata = FileMetadata.objects.create(
            original_file_name=file.name,
            server_file_path=server_file_path,
            file_size_bytes=os.path.getsize(server_file_path),
            file_extension=file_extension,
            table_metadata_id=table_metadata_id,
        )

        file_metadata.save()
        return file_metadata

    def delete(self, *args, **kwargs) -> None:
        """Overriding the default delete method as the file should be deleted as well.

        We want to delete the actual file, when the metadata for a file is deleted. We
        can do this by overriding the default delete method and adding som extra
        behaviour.

        Args:
            *args: The positional arguments required by Django
            **kwargs: The keyword arguments required by Django
        """
        # The normal delete logic is called:
        super().delete(*args, **kwargs)

        # And we delete the file
        os.remove(self.server_file_path)

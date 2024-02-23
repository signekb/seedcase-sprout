"""File for testing FileMetadata."""
import io
import os

from django.test import TestCase

from sprout.models.file_metadata import FileMetaData
from sprout.tests.db_test_utils import create_table


class FileMetaDataTests(TestCase):
    """File with test cases."""

    def test_persist_file(self):
        """Testing the persistence of file and its metadata."""
        # Arrange
        file = io.BytesIO(b"A file with some content")
        file.name = "my-file.csv"
        test_table = create_table("TestTable")
        test_table.save()

        # Act
        file_meta = FileMetaData.persist_raw_file(file, test_table.id)

        # Assert
        self.assertEqual(file.name, file_meta.original_file_name)
        self.assertEqual("csv", file_meta.file_extension)
        self.assertTrue(file_meta.server_file_path.startswith("persistent_storage/raw"))
        self.assertTrue(file_meta.server_file_path.endswith(".csv"))
        self.assertTrue(os.path.exists(file_meta.server_file_path))
        # We clean up again
        os.remove(file_meta.server_file_path)

"""Tests for table_files."""

import io

from django.test import TestCase
from django.urls import reverse

from sprout.models import FileMetadata
from sprout.tests.db_test_utils import create_table


class TableFilesTests(TestCase):
    """Tests for table_files."""

    def test_overview_should_show_files_for_table(self):
        """The rendered overview should show file.csv on the page."""
        # Arrange
        table = create_table("TestTable")
        table.save()
        file = io.BytesIO(b"File content")
        file.name = "file.csv"
        file_meta = FileMetadata.create_file_metadata(file, table.id)
        url = reverse("table-files", kwargs={"table_id": table.id})

        # Act
        response = self.client.post(url)

        # Assert
        self.assertContains(response, file.name)
        file_meta.delete()

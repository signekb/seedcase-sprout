import io
import os

from django.test import TestCase

from config.settings import PERSISTENT_STORAGE_PATH
from sprout.uploaders import upload_raw_file


class TestUploadRawDataFile(TestCase):
    def setUp(self):
        self.file = io.BytesIO(b"A file with some content")
        self.file.name = "fake-test-file.csv"
        self.expected_file = "fake.test.csv"
        self.expected_path = f"{PERSISTENT_STORAGE_PATH}/raw/{self.expected_file}"

    def test_upload_raw_file(self):
        result_path = upload_raw_file(self.file, self.expected_file)
        self.assertEqual(result_path, self.expected_path)
        self.assertTrue(os.path.isfile(self.expected_path))

    def tearDown(self):
        # Clean up created file after test
        os.remove(self.expected_path)

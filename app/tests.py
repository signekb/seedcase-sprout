from django.test import TestCase

# Note: Two types of TestCase: django.test or unittest
# https://docs.djangoproject.com/en/5.0/topics/testing/overview/
class SmokeTest(TestCase):
    def test_smoke(self):
        self.assertTrue(True)


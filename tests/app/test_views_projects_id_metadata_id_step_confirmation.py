from django.test import TestCase
from django.urls import reverse

from sprout.app.models import Tables
from sprout.app.views.projects_id_metadata_id.helpers import create_stepper_url
from tests.db_test_utils import create_table


class MetadataStepConfirmationTests(TestCase):
    def setUp(self):
        self.table = create_table("TableName")
        self.table.save()

        self.current_url = create_stepper_url(4, self.table.id)
        self.redirect_url = reverse("projects-id-metadata-view")

    def tests_confirmation_step_is_rendered(self):
        """Check if confirmation page is rendered."""
        # Act
        response = self.client.get(self.current_url)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.table.name)

    def tests_confirmation_step_redirect(self):
        """Check redirect on post and is_draft is False."""
        # Act
        response = self.client.post(self.current_url)

        # Assert
        self.assertRedirects(response, self.redirect_url)
        self.assertFalse(Tables.objects.get(name=self.table.name).is_draft)

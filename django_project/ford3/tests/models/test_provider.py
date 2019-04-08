from django.test import TestCase
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories


class TestProvider(TestCase):

    def setUp(self):
        self.new_provider = ModelFactories.get_provider_test_object()

    def test_provider_description_save_and_read(self):

        self.assertEqual(str(self.new_provider), 'Object Test Name')

    def test_correct_GET_template_used(self):
        url = reverse(
                'edit-provider',
                kwargs={
                    'provider_id': self.new_provider.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'provider_form.html')

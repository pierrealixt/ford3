from rest_framework.reverse import reverse
from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestProviderViewSet(TestCase):

    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object()
        self.url = reverse('show-providers-api', kwargs={'version': 'v1'})

    def test_show_providers_api(self):
        response = self.client.get(self.url)
        body = str(response.content)
        self.assertIn(self.provider.name, body)

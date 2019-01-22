from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestProvider(TestCase):

    def test_provider_description(self):
        new_provider = ModelFactories.get_provider_test_object()
        self.assertEqual(new_provider.__str__(), 'Object Test Name')

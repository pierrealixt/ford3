from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestModule(TestCase):

    def test_module_description(self):
        new_module = ModelFactories.get_module_test_object()
        self.assertEqual(new_module.__str__(), 'Object Test Name')

from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestOccupation(TestCase):

    def test_occupation_description(self):
        new_occupation = ModelFactories.get_occupation_test_object()
        self.assertEqual(new_occupation.__str__(), 'Object Test Name')

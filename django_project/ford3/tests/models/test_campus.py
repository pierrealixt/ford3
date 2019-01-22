from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestCampus(TestCase):

    def test_campus_description(self):
        new_campus = ModelFactories.get_campus_test_object()
        self.assertEqual(new_campus.__str__(), 'Object Test Name')

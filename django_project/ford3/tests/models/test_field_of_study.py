from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestFieldOfStudy(TestCase):

    def test_field_of_study_description(self):
        new_field_of_study = ModelFactories.get_field_of_study_test_object()
        self.assertEqual(new_field_of_study.__str__(), 'Object Test Name')

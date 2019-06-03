from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestSubFieldOfStudy(TestCase):

    def test_sub_field_of_study_description(self):
        new_sub_f_study = ModelFactories.get_sub_field_of_study_test_object()
        self.assertEqual(new_sub_f_study.__str__(), 'Object Test Name')

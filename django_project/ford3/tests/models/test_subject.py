from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestSubject(TestCase):

    def test_subject_description(self):
        new_subject = ModelFactories.get_subject_test_object()
        self.assertEqual(new_subject.__str__(), 'Object Test Name')

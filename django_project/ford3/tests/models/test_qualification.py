from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestQualification(TestCase):

    def test_qualification_name(self):
        new_qualification = ModelFactories.get_qualification_test_object()
        self.assertEqual(str(new_qualification), 'SAQAQualification name')

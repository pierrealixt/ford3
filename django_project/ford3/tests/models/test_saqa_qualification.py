from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestSAQAQualification(TestCase):

    def test_saqa_qualification_description(self):
        new_saqa_qualification = (
            ModelFactories.get_saqa_qualification_test_object())
        self.assertEqual(new_saqa_qualification.__str__(),
            """SAQAQualification name"""
        )

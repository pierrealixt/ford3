from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestQualification(TestCase):
    def setUp(self):
        self.qualification = ModelFactories.get_qualification_test_object()

    def test_qualification_name(self):
        self.assertEqual(
            str(self.qualification),
            'SAQAQualification name')


class TestQualificationOccupations(TestCase):
    def setUp(self):
        self.qualification = ModelFactories.get_qualification_test_object()
        self.occupation = ModelFactories.get_occupation_test_object()

    def test_toggle_occupations(self):

        # ModelFactories.get_qualification_test_object()
        # already adds one occupation
        self.assertEqual(self.qualification.occupations.count(), 1)

        occupation_ids = ' '.join([
            str(self.occupation.id)
        ])

        self.qualification.toggle_occupations(occupation_ids)
        self.assertEqual(self.qualification.occupations.count(), 1)

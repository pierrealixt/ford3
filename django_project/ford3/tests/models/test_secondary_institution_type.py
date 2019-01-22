from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestSecondaryInstitutionType(TestCase):

    def test_secondary_institution_type_name(self):
        new_secondary_institution_type = (
            ModelFactories.get_secondary_institution_type_test_object())
        self.assertEqual(
            new_secondary_institution_type.__str__(),
            'Object Test Name')

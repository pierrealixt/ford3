from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.saqa_qualification import SAQAQualification
from django.core.exceptions import ValidationError


class TestSAQAQualification(TestCase):

    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object()
        self.fos = ModelFactories.get_field_of_study_test_object()
        self.data = {
            'name': 'Non-official Bachelor of Arts',
            'provider_id': self.provider.id,
            'fos_id': self.fos.id
        }

    def test_saqa_qualification_description(self):
        new_saqa_qualification = (
            ModelFactories.get_saqa_qualification_test_object())
        self.assertEqual(
            new_saqa_qualification.__str__(),
            'SAQAQualification name')

    def test_create_non_accredited_saqa_qualification(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        saqa_qualif = SAQAQualification.create_non_accredited(self.data)

        self.assertFalse(saqa_qualif.accredited)
        self.assertEqual(saqa_qualif.creator_provider_id, self.provider.id)
        self.assertEqual(saqa_qualif.field_of_study_id, self.fos.id)
        self.assertIsNone(saqa_qualif.sub_field_of_study)
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

    def test_create_non_accredited_saqa_qualification_with_subfield(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        sfos = ModelFactories.get_sub_field_of_study_test_object()
        self.data['fos_id'] = sfos.field_of_study.id
        self.data['sfos_id'] = sfos.id
        saqa_qualif = SAQAQualification.create_non_accredited(self.data)

        self.assertFalse(saqa_qualif.accredited)
        self.assertEqual(saqa_qualif.creator_provider_id, self.provider.id)

        self.assertEqual(saqa_qualif.field_of_study_id, sfos.field_of_study.id)
        self.assertEqual(saqa_qualif.sub_field_of_study_id, sfos.id)

        self.assertEqual(len(SAQAQualification.objects.all()), 1)

    def test_create_duplicate_non_accredited_saqa_qualification(self):

        SAQAQualification.create_non_accredited(self.data)

        with self.assertRaises(ValidationError):
            SAQAQualification.create_non_accredited(self.data)

    def test_create_accredited_saqa_qualification(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        saqa_qualif = SAQAQualification.create_accredited(
            name='Official Bachelor of Arts',
            saqa_id=42042)

        self.assertTrue(saqa_qualif.accredited)
        self.assertNotEqual(saqa_qualif.id, saqa_qualif.saqa_id)
        self.assertIsNone(saqa_qualif.creator_provider_id)
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

    def test_get_or_create_accredited_saqa_qualification(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        saqa = {
            'saqa_id': 59731,
            'name': 'Champagne'
        }
        # it should create a SAQA qualification
        saqa_qualif = SAQAQualification.get_or_create_accredited(saqa)

        self.assertEqual(
            saqa_qualif.saqa_id,
            saqa['saqa_id'])
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

        # it should return the same qualification
        saqa_qualif_again = SAQAQualification.get_or_create_accredited(saqa)
        self.assertEqual(saqa_qualif_again.id, saqa_qualif.id)
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

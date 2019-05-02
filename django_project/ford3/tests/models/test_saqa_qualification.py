from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.saqa_qualification import SAQAQualification


class TestSAQAQualification(TestCase):

    def test_saqa_qualification_description(self):
        new_saqa_qualification = (
            ModelFactories.get_saqa_qualification_test_object())
        self.assertEqual(new_saqa_qualification.__str__(),
            """SAQAQualification name"""
        )

    def test_create_non_accredited_saqa_qualification(self):

        provider = ModelFactories.get_provider_test_object()

        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        saqa_qualif = SAQAQualification.create_non_accredited(
            name='Non-official Bachelor of Arts',
            creator_provider=provider)


        self.assertFalse(saqa_qualif.accredited)
        self.assertEqual(saqa_qualif.id, saqa_qualif.saqa_id)
        self.assertEqual(saqa_qualif.creator_provider_id, provider.id)
        self.assertEqual(len(SAQAQualification.objects.all()), 1)


    def test_create_accredited_saqa_qualification(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        saqa_qualif = SAQAQualification.create_accredited(
            name='Official Bachelor of Arts',
            saqa_id=42042)

        self.assertTrue(saqa_qualif.accredited)
        self.assertNotEqual(saqa_qualif.id, saqa_qualif.saqa_id)
        self.assertIsNone(saqa_qualif.creator_provider_id)
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

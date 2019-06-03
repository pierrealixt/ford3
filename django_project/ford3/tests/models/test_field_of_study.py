from django.test import TestCase
from ford3.models.field_of_study import FieldOfStudy
from ford3.tests.models.model_factories import ModelFactories


class TestFieldOfStudy(TestCase):
    def setUp(self):
        self.field_of_study = ModelFactories.get_field_of_study_test_object()

    def test_field_of_study_description(self):
        self.assertEqual(
            self.field_of_study.__str__(),
            'Object Test Name')

    def test_get_or_create(self):
        # it should get
        fos, created = FieldOfStudy.objects.get_or_create(
            name=self.field_of_study)
        self.assertEqual(fos.id, self.field_of_study.id)
        self.assertFalse(created)

        # it should create
        fos, created = FieldOfStudy.objects.get_or_create(
            name='Manufacturing, Engineering and Technology')
        self.assertNotEqual(fos.id, self.field_of_study.id)
        self.assertTrue(created)
        self.assertEqual(len(FieldOfStudy.objects.all()), 2)

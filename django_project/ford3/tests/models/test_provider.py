from django.test import TestCase
from django.core.exceptions import ValidationError
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.user import User

from ford3.models.campus import Campus
from ford3.models.qualification import Qualification


class TestProviderSoftDelete(TestCase):
    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object()
        self.campus1 = ModelFactories.get_campus_test_object()
        self.campus2 = ModelFactories.get_campus_test_object()
        self.qualification1 = ModelFactories.get_qualification_test_object()
        self.qualification2 = ModelFactories.get_qualification_test_object()
        self.qualification3 = ModelFactories.get_qualification_test_object()
        self.campus1.provider = self.provider
        self.campus2.provider = self.provider
        self.qualification1.campus = self.campus1
        self.qualification2.campus = self.campus2
        self.qualification3.campus = self.campus2
        self.campus1.save()
        self.campus2.save()
        self.qualification1.save()
        self.qualification2.save()
        self.qualification3.save()

    def test_soft_delete_provider(self):
        self.assertFalse(self.provider.deleted)
        self.assertFalse(self.campus1.deleted)
        self.assertFalse(self.campus2.deleted)
        self.assertFalse(self.qualification1.deleted)
        self.assertFalse(self.qualification2.deleted)
        self.assertFalse(self.qualification3.deleted)
        self.provider.soft_delete()
        self.assertTrue(self.provider.deleted)
        self.update_objects()
        self.assertTrue(self.campus1.deleted)
        self.assertTrue(self.qualification1.deleted)
        self.assertTrue(self.qualification2.deleted)
        self.assertTrue(self.qualification3.deleted)

    def update_objects(self):
        self.campus1 = Campus.objects.get(pk=self.campus1.id)
        self.campus2 = Campus.objects.get(pk=self.campus2.id)
        self.qualification1 = Qualification.objects.get(
            pk=self.qualification1.id)
        self.qualification2 = Qualification.objects.get(
            pk=self.qualification2.id)
        self.qualification3 = Qualification.objects.get(
            pk=self.qualification3.id)


class TestProvider(TestCase):

    def setUp(self):
        self.new_provider = ModelFactories.get_provider_test_object()
        self.user = User(
            'bobby', 'bobby@kartoza.com', 'bob')

    def test_provider_description_save_and_read(self):
        self.assertEqual(str(self.new_provider), 'Object Test Name')

    def test_is_new_provider(self):
        self.assertTrue(self.new_provider.is_new_provider)

        campus = ModelFactories.get_campus_test_object()
        campus.provider_id = self.new_provider.id
        campus.save()

        self.assertEqual(self.new_provider.id, campus.provider_id)

        self.assertFalse(self.new_provider.is_new_provider)


class TestCreateUniqueProvider(TestCase):
    def test_create_duplicate_model(self):
        self.provider2 = ModelFactories.get_provider_test_object()
        self.provider1 = ModelFactories.get_provider_test_object()
        self.provider1.name = self.provider2.name
        with self.assertRaises(ValidationError):
            self.provider1.save()

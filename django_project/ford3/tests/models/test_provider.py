from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.user import User
from django.core.exceptions import ValidationError


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

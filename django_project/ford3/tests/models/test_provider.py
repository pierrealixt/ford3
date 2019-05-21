from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories


class TestProvider(TestCase):

    def setUp(self):
        self.new_provider = ModelFactories.get_provider_test_object()
        self.user = User.objects.create_user(
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

    def test_correct_GET_template_used(self):
        url = reverse(
                'edit-provider',
                kwargs={
                    'provider_id': self.new_provider.id})
        response = self.client.get(url)
        # redirect when not logged in
        self.assertEqual(response.status_code, 302)
        self.client.login(username="bobby", password="bob")
        # get provider form when logged in
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'provider_form.html')

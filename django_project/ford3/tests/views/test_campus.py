from django.urls import reverse
from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestCreateCampusView(TestCase):

    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object()
        self.url = reverse('create-campus', args=[str(self.provider.id)])

        self.data = {
            'campus_name': 'My Campus'
        }

    def test_create_campus(self):
        response = self.client.post(self.url, self.data)

        self.assertIn(self.data['campus_name'], str(response.content))

    def test_create_duplicate_campus(self):
        self.provider.campus_set.create(name=self.data['campus_name'])

        response = self.client.post(self.url, self.data)

        self.assertIn(self.data['campus_name'], str(response.content))

        self.assertIn('Name is already taken.', str(response.content))

    def test_create_empty_campus(self):
        response = self.client.post(self.url, {'campus_name': ''})

        self.assertIn('Name is required.', str(response.content))

    def test_create_wrong_argument(self):
        response = self.client.post(
            self.url,
            {'another_campus_name': 'My Campus'})

        self.assertIn('Bad request.', str(response.content))

    def test_forbid_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        # it should redirect to provider.
        provider_url = reverse('show-provider', args=[str(self.provider.id)])
        self.assertRedirects(response, provider_url, target_status_code=302)

    def test_show_success(self):
        response = self.client.post(self.url, self.data)

        self.assertIn('Campus successfully created.', str(response.content))

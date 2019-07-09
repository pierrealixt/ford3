from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.user import User
from django.contrib.auth.models import Group


class TestCreateCampusView(TestCase):
    fixtures = ['groups', 'sa_provinces']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'email@email.com', 'password', is_provider=True, is_active=True)
        self.user.groups.add(Group.objects.get(name='PROVIDER-ADMINS'))
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_campus'))

        self.provider = ModelFactories.get_provider_test_object()
        self.provider.created_by = self.user
        self.provider.save()
        self.url = reverse('create-campus', args=[str(self.provider.id)])

        self.data = {
            'campus_name': 'My Campus'
        }
        self.client.login(
            email=self.user.email,
            password='password')


    def test_create_campus(self):
        response = self.client.post(self.url, self.data, follow=True)
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
        self.assertRedirects(response, provider_url, target_status_code=200)

    def test_show_success(self):
        response = self.client.post(self.url, self.data)

        self.assertIn('Campus successfully created.', str(response.content))

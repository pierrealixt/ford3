from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase, Client
from ford3.models.provider import Provider
from ford3.tests.models.model_factories import ModelFactories


class TestDashboard(TestCase):
    fixtures = [
        'groups',
        'sa_provinces'
    ]

    # 'test_province_users',
    # 'test_provider_users',
    # 'test_campus_users',

    def setUp(self):
        self.client = Client()
        self.users = [
            ModelFactories.create_user_province(),
            ModelFactories.create_user_provider(),
            ModelFactories.create_user_campus()
        ]
        call_command('loaddata', 'test_providers.json', verbosity=0)
        self.provider = Provider.objects.get(pk=1)

        self.users[2].creator_id = self.users[1]
        self.users[2].save()
        self.url = reverse('dashboard')

    def runTest(self):
        """
        The three users (province, provider, campus) should see the same provider.
        """ # noqa

        for user in self.users:
            self.client.login(email=user.email, password='password')
            response = self.client.get(self.url)
            self.assertIn(self.provider.name, str(response.content))

from django.urls import reverse
from django.test import TestCase
from ford3.models.user import User
from ford3.models.provider import Provider


class TestDashboard(TestCase):
    fixtures = [
        'groups',
        'sa_provinces',
        'test_province_users',
        'test_provider_users',
        'test_campus_users',
        'test_providers'
    ]

    def setUp(self):
        self.users_ids = [1, 2, 3]
        self.provider = Provider.objects.get(pk=1)

        self.url = reverse('dashboard')

    def runTest(self):
        """
        The three users (province, provider, campus) should see the same provider.
        """
        for user_id in self.users_ids:
            user = User.objects.get(pk=user_id)
            self.client.force_login(user, backend=None)
            response = self.client.get(self.url)
            self.assertIn(self.provider.name, str(response.content))

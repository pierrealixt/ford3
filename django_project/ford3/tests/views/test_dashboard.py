from django.urls import reverse
from django.test import TestCase, Client
from ford3.models.provider import Provider
from ford3.models.user import User


class TestDashboard(TestCase):
    fixtures = [
        'groups',
        'sa_provinces',
        'test_providers',
        'test_province_users',
        'test_provider_users',
        'test_campus_users'
    ]

    def setUp(self):
        self.client = Client()
        self.provider = Provider.objects.get(pk=1)
        self.url = reverse('dashboard')
        for user in User.objects.all():
            user.set_password(user.password)
            user.is_active = True
            user.save()

    def runTest(self):
        """
        The three users (province, provider, campus) should see the same provider.
        """ # noqa

        for user in User.objects.all():
            self.client.login(email=user.email, password='password')
            response = self.client.get(self.url, follow=True)
            self.assertIn(self.provider.name, str(response.content))

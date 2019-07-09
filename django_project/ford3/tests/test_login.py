from django.test import Client, TestCase
from django.contrib.auth.models import Group
from ford3.models.user import User


class TestLoginWithCreateUser(TestCase):
    fixtures = [
        'groups',
        'sa_provinces'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'email@email.com', 'password', is_province=True, is_active=True)
        self.user.groups.add(Group.objects.get(name='PROVINCE-ADMINS'))

    def runTest(self):
        response = self.client.get('/', follow=True)
        self.assertTrue('Login' in str(response.content))

        self.assertTrue(
            self.client.login(email=self.user.email, password='password'))

        response = self.client.get('/', follow=True)
        self.assertTrue('Logout' in str(response.content))


class TestLoginWithFixtures(TestCase):
    fixtures = [
        'groups',
        'sa_provinces',
        'test_province_users',
    ]

    def setUp(self):
        self.client = Client()
        for user in User.objects.all():
            user.set_password(user.password)
            user.is_active = True
            user.save()

        self.user = User.objects.get(pk=1)

    def runTest(self):
        response = self.client.get('/', follow=True)
        self.assertTrue('Login' in str(response.content))

        self.assertTrue(
            self.client.login(email=self.user.email, password='password'))

        response = self.client.get('/', follow=True)
        self.assertTrue('Logout' in str(response.content))

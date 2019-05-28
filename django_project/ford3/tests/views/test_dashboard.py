from django.urls import reverse
from django.contrib.auth.models import Group
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.province import Province


class TestProviderDashboard(TestCase):
    def setUp(self):
        call_command('loaddata', 'provinces_group')
        call_command('loaddata', 'providers_group')
        call_command('loaddata', 'campus_group')
        call_command('loaddata', 'sa_provinces')
        self.url = reverse('dashboard')

        self.province = Province.objects.get(pk=1)
        self.provider1 = ModelFactories.get_provider_test_object()
        self.provider2 = ModelFactories.get_provider_test_object()
        self.provider3 = ModelFactories.get_provider_test_object()
        self.provider4 = ModelFactories.get_provider_test_object()
        self.provider1.province = self.province
        self.provider2.province = self.province
        self.provider3.province = self.province
        self.provider4.province = self.province
        self.provider1.name = 'Provider One'
        self.provider2.name = 'Provider Two'
        self.provider3.name = 'Provider Three'
        self.provider4.name = 'Provider Four'
        self.campus1 = (
            ModelFactories.get_campus_test_object_with_name(
                name='campus1', provider=self.provider1))
        self.campus2 = (
            ModelFactories.get_campus_test_object_with_name(
                name='campus2', provider=self.provider1))
        self.campus3 = (
            ModelFactories.get_campus_test_object_with_name(
                'campus3', self.provider1))
        self.campus4 = (
            ModelFactories.get_campus_test_object_with_name(
                'campus4', self.provider2))
        self.campus5 = (
            ModelFactories.get_campus_test_object_with_name(
                'campus5', self.provider2))
        self.campus6 = (
            ModelFactories.get_campus_test_object_with_name(
                'campus6', self.provider3))
        self.campus7 = (
            ModelFactories.get_campus_test_object_with_name(
                'campus7', self.provider4))

        self.province_user = (
            self.create_temp_province_user(self.province, "temp_province"))
        self.provider_user1 = (
            self.create_temp_provider_user(self.province_user,
                                           "temp_provider_1"))
        self.provider_user2 = (
            self.create_temp_provider_user(self.province_user,
                                           "temp_provider_2"))

        self.campus_user_1 = (
            self.create_temp_campus_user(self.provider_user2,
                                         "temp_campus_1"))
        self.temp_user = self.create_temp_groupless_user("temp_user")

        self.provider1.users.add(self.province_user)
        self.provider2.users.add(self.province_user)
        self.provider3.users.add(self.province_user)
        self.provider4.users.add(self.province_user)

        self.provider1.users.add(self.provider_user1)
        self.provider2.users.add(self.provider_user1)
        self.provider1.creator = self.provider_user1
        self.provider2.creator = self.provider_user1

        self.provider3.users.add(self.provider_user2)
        self.provider4.users.add(self.provider_user2)
        self.provider3.creator = self.provider_user2
        self.provider4.creator = self.provider_user2

        self.provider1.save()
        self.provider2.save()
        self.provider3.save()
        self.provider4.save()

    def test_basic_authentication(self):
        status_code = self.client.get(self.url).status_code
        self.assertEqual(302, status_code)

    def test_show_with_no_group(self):
        login_result = self.client.login(
            username=self.temp_user.username, password='temp')
        self.assertTrue(login_result)
        status_code = self.client.get(self.url).status_code
        self.assertEqual(302, status_code)

    def test_show_as_province(self):
        login_result = self.client.login(
            username=self.province_user.username, password='temp')
        self.assertTrue(login_result)
        response = self.client.get(self.url)
        body = str(response.content)
        self.assertIn(self.provider1.name, body)
        self.assertIn(self.provider2.name, body)
        self.assertIn(self.provider3.name, body)
        self.assertIn(self.provider4.name, body)

    def test_show_as_provider(self):
        login_result = self.client.login(
            username=self.provider_user1.username, password='temp')
        self.assertTrue(login_result)
        response = self.client.get(self.url)
        body = str(response.content)
        self.assertIn(self.provider1.name, body)
        self.assertIn(self.provider2.name, body)
        self.assertNotIn(self.provider3.name, body)
        self.assertNotIn(self.provider4.name, body)
        self.fail(body)

    def test_show_as_campus(self):
        login_result = self.client.login(
            username=self.campus_user_1.username, password='temp')
        self.assertTrue(login_result)
        response = self.client.get(self.url)
        body = str(response.content)
        self.assertNotIn(self.provider1.name, body)
        self.assertNotIn(self.provider2.name, body)
        self.assertIn(self.provider3.name, body)
        self.assertIn(self.provider4.name, body)

    def create_temp_province_user(self, province: Province, username):
        user = get_user_model().objects.create_user(
            username,
            'temp',
            'temp@temp.com')
        user.set_password('temp')
        provinces_group: Group = Group.objects.get(pk=1)
        user.groups.add(provinces_group)
        user.save()
        user.is_province = True
        province.users.add(user)
        return user

    def create_temp_provider_user(self, province_user, username):
        user = get_user_model().objects.create_user(
            username,
            'temp',
            'temp2@temp.com')
        user.set_password('temp')
        province = self.get_user_province(province_user)
        province.users.add(user)
        provider_group: Group = Group.objects.get(pk=3)
        user.groups.add(provider_group)
        user.is_provider = True
        user.save()
        return user

    def create_temp_campus_user(self, provider_user, username):
        user = get_user_model().objects.create_user(
            username,
            'temp',
            'temp3@temp.com')
        user.set_password('temp')
        province = self.get_user_province(provider_user)
        province.users.add(user)
        campus_group: Group = Group.objects.get(pk=2)
        user.groups.add(campus_group)
        user.is_campus = True
        user.creator = provider_user
        user.save()

        return user

    def create_temp_groupless_user(self, username):
        user = get_user_model().objects.create_user(
            username,
            'temp',
            'temp3@temp.com')
        user.set_password('temp')

        user.save()
        return user

    def get_user_province(self, user):
        province = Province.objects.filter(users__id=user.id).first()
        return province

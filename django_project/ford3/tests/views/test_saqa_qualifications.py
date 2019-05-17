import json
from django.urls import reverse
from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestCreateSaqaQualificationsView(TestCase):
    def setUp(self):
        self.url = reverse('create-saqa-qualification')
        self.provider = ModelFactories.get_provider_test_object()
        self.fos = ModelFactories.get_field_of_study_test_object()
        self.saqa_qualification_name = 'Master Degree in Wine and Champagne'

        self.data = {
            'saqa_qualification_name': self.saqa_qualification_name,
            'provider_id': self.provider.id,
            'fos_id': self.fos.id
        }

    def test_bad_request(self):
        del self.data['fos_id']
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_qualification(self):
        response = self.client.post(self.url, self.data)

        content = json.loads(response.content)

        self.assertEqual(content['success'], True)
        self.assertEqual(
            content['saqa_qualification']['name'],
            self.saqa_qualification_name)

    def test_create_duplicate_qualification(self):
        self.client.post(self.url, self.data)

        # create with same data
        response = self.client.post(self.url, self.data)
        content = json.loads(response.content)

        # it should fail
        self.assertEqual(content['success'], False)
        self.assertEqual(
            content['error'],
            'Non-accredited SAQA qualification name must be unique per provider.') # noqa

    def test_create_qualification_with_empty_name(self):
        data = {
            'saqa_qualification_name': '',
            'provider_id': self.provider.id,
            'fos_id': self.fos.id
        }

        response = self.client.post(self.url, data)
        content = json.loads(response.content)

        self.assertEqual(content['success'], False)
        self.assertEqual(content['error'], 'Name is required.')


class TestSearchSaqaQualificationsView(TestCase):
    def setUp(self):
        self.saqa = ModelFactories.get_saqa_qualification_test_object()

    def test_search_by_saqa_id(self):
        query = 'q={}'.format(self.saqa.saqa_id)

        response = self.client.get(
            '{url}?{query}'.format(
                url=reverse('search-saqa-qualifications'),
                query=query))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 1)
        self.assertEqual(
            content['results'][0]['name'],
            self.saqa.name)

    def test_search_by_name(self):
        query = 'q={}'.format(self.saqa.name[0:8])

        response = self.client.get(
            '{url}?{query}'.format(
                url=reverse('search-saqa-qualifications'),
                query=query))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 1)
        self.assertEqual(
            content['results'][0]['name'],
            self.saqa.name)

    def test_search_by_name_case_insensitive_lower(self):
        query = 'q={}'.format(self.saqa.name[0:8].lower())

        response = self.client.get(
            '{url}?{query}'.format(
                url=reverse('search-saqa-qualifications'),
                query=query))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 1)
        self.assertEqual(
            content['results'][0]['name'],
            self.saqa.name)

    def test_search_by_name_case_insensitive_upper(self):
        query = 'q={}'.format(self.saqa.name[0:8].upper())

        response = self.client.get(
            '{url}?{query}'.format(
                url=reverse('search-saqa-qualifications'),
                query=query))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 1)
        self.assertEqual(
            content['results'][0]['name'],
            self.saqa.name)

    def test_search_empty_query(self):
        query = 'q='
        response = self.client.get(
            '{url}?{query}'.format(
                url=reverse('search-saqa-qualifications'),
                query=query))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 0)

    def test_search_without_query(self):

        response = self.client.get(
            '{url}'.format(
                url=reverse('search-saqa-qualifications')))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 0)

    def test_search_as_post(self):
        response = self.client.post(
            '{url}?'.format(
                url=reverse('search-saqa-qualifications')))

        content = json.loads(response.content)

        self.assertEqual(len(content['results']), 0)

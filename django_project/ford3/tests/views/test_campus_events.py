import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from ford3.models.campus_event import CampusEvent
from ford3.models.campus import Campus


from ford3.tests.models.model_factories import ModelFactories


class TestCreateCampusEventView(TestCase):
    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object()
        self.url = reverse('create-or-update-event',
                           args=[str(self.campus.id), 'campus'])
        self.data = {
                    'name': 'TestName',
                    'date_start': '2999-10-14',
                    'date_end': '2999-10-15',
                    'http_link': ''}

    def test_create_event(self):
        self.assertEqual(len(self.campus.events), 0)
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(body['success'], True)
        self.assertEqual(
            body['event']['id'], self.campus.events[0]['id'])
        self.assertEqual(len(self.campus.events), 1)

    def test_create_event_empty_name(self):
        self.data['name'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_empty_date_start(self):
        self.data['date_start'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_empty_date_end(self):
        self.data['date_end'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_empty_http_link(self):
        self.data['http_link'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 1)

    def test_create_event_invalid_http_link(self):
        self.data['http_link'] = 'I am invalid'
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertFalse(body['success'])
        self.assertIn('Enter a valid URL.', ','.join(body['error_msg']))
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_invalid_date_start(self):
        self.data['date_start'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_invalid_date_end(self):
        self.data['date_end'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_end_before_start_fails(self):
        self.data['date_start'] = '2018-04-10'
        self.data['date_end'] = '2016-04-10'
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(len(self.campus.events), 0)
        self.assertIn(
            'The start date must be before the end date',
            body['error_msg'])

    def test_create_past_event_fails(self):
        self.data['date_start'] = (
                datetime.now() - timedelta(days=2)).date().isoformat()
        self.data['date_end'] = (
                datetime.now() - timedelta(days=1)).date().isoformat()
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)


class TestUpdateCampusEventView(TestCase):
    def setUp(self):
        self.campus_event = ModelFactories.get_campus_event_test_object()
        self.url = reverse(
            'create-or-update-event',
            args=[str(self.campus_event.id), 'campus'])
        self.data = {
            'id': self.campus_event.id,
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}

    def test_update_event(self):
        self.assertNotEqual(self.campus_event.name, self.data['name'])
        self.client.post(self.url, self.data)
        self.campus_event = CampusEvent.objects.get(pk=self.campus_event.id)
        self.assertEqual(self.campus_event.name, self.data['name'])


class TestDeleteCampusEventView(TestCase):
    def setUp(self):

        self.campus_event = ModelFactories.get_campus_event_test_object()
        self.campus: Campus = self.campus_event.campus
        self.url = reverse(
            'delete-event', args=['campus'])
        self.data = {
            'id': self.campus_event.id,
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}

    def test_delete_event(self):
        self.assertEqual(len(self.campus.events), 1)
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertTrue(body['success'])
        self.campus = Campus.objects.get(pk=self.campus.id)
        self.assertEqual(len(self.campus.events), 0)

    def test_delete_event_without_id(self):
        self.data = {
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertFalse(body['success'])

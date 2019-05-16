import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from ford3.models.campus_event import CampusEvent


from ford3.tests.models.model_factories import ModelFactories


class TestCreateCampusEventView(TestCase):
    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object()
        self.url = reverse('create-or-update-campus-event', args=[str(self.campus.id)])
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
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_invalid_date_start(self):
        self.data['date_start'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_invalid_date_start(self):
        self.data['date_end'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

    def test_create_event_end_before_start_fails(self):
        self.data['date_start'] = '2018-04-10'
        self.data['date_end'] = '2016-04-10'
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(len(self.campus.events), 0)
        self.assertEqual(
            body['error_msg'],
            'The start date must be before the end date')

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
            'create-or-update-campus-event', args=[str(self.campus_event.id)])
        self.data = {
            'id': self.campus_event.id,
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}
        self.client.post(self.url, self.data)

    def test_update_event(self):
        self.assertNotEqual(self.campus_event.name, self.data['name'])
        self.client.post(self.url, self.data)
        self.campus_event = CampusEvent.objects.get(pk=self.campus_event.id)
        self.assertEqual(self.campus_event.name, self.data['name'])

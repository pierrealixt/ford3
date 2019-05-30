import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from ford3.models.qualification_event import QualificationEvent
from ford3.models.qualification import Qualification


from ford3.tests.models.model_factories import ModelFactories


class TestCreateQualificationEventView(TestCase):
    def setUp(self):
        self.qualification = ModelFactories.get_qualification_test_object()
        self.url = reverse('create-or-update-event',
                           args=[str(self.qualification.id), 'qualification'])
        self.data = {
                    'name': 'TestName',
                    'date_start': '2999-10-14',
                    'date_end': '2999-10-15',
                    'http_link': ''}

    def test_create_event(self):
        self.assertEqual(len(self.qualification.events), 0)
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(body['success'], True)
        self.assertEqual(
            body['event']['id'], self.qualification.events[0]['id'])
        self.assertEqual(len(self.qualification.events), 1)

    def test_create_event_empty_name(self):
        self.data['name'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_empty_date_start(self):
        self.data['date_start'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_empty_date_end(self):
        self.data['date_end'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_empty_http_link(self):
        self.data['http_link'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 1)

    def test_create_event_invalid_http_link(self):
        self.data['http_link'] = 'I am invalid'
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertFalse(body['success'])
        self.assertIn('Enter a valid URL.', ','.join(body['error_msg']))
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_invalid_date_start(self):
        self.data['date_start'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_invalid_date_end(self):
        self.data['date_end'] = 'I am invalid'
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)

    def test_create_event_end_before_start_fails(self):
        self.data['date_start'] = '2018-04-10'
        self.data['date_end'] = '2016-04-10'
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(len(self.qualification.events), 0)
        self.assertIn(
            'The start date must be before the end date',
            body['error_msg'])

    def test_create_past_event_fails(self):
        self.data['date_start'] = (
                datetime.now() - timedelta(days=2)).date().isoformat()
        self.data['date_end'] = (
                datetime.now() - timedelta(days=1)).date().isoformat()
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.qualification.events), 0)


class TestUpdateQualificationEventView(TestCase):
    def setUp(self):
        self.qualification_event = (
            ModelFactories.get_qualification_event_test_object())
        self.url = reverse(
            'create-or-update-event',
            args=[str(self.qualification_event.id), 'qualification'])
        self.data = {
            'id': self.qualification_event.id,
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}

    def test_update_event(self):
        self.assertNotEqual(self.qualification_event.name, self.data['name'])
        self.client.post(self.url, self.data)
        self.qualification_event = QualificationEvent.objects.get(
            pk=self.qualification_event.id)
        self.assertEqual(self.qualification_event.name, self.data['name'])


class TestDeleteQualificationEventView(TestCase):
    def setUp(self):

        self.qualification_event = (
            ModelFactories.get_qualification_event_test_object())
        self.qualification: Qualification = (
            self.qualification_event.qualification)
        self.url = reverse(
            'delete-event', args=['qualification'])
        self.data = {
            'id': self.qualification_event.id,
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}

    def test_delete_event(self):
        self.assertEqual(len(self.qualification.events), 1)
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertTrue(body['success'])
        self.qualification = Qualification.objects.get(
            pk=self.qualification.id)
        self.assertEqual(len(self.qualification.events), 0)

    def test_delete_event_without_id(self):
        self.data = {
            'name': 'TestName',
            'date_start': '2999-04-14',
            'date_end': '2999-04-15',
            'http_link': ''}
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertFalse(body['success'])

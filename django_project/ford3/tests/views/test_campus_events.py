import json
from django.test import TestCase
from django.urls import reverse


from ford3.tests.models.model_factories import ModelFactories


class TestCreateCampusEventView(TestCase):
    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object()
        self.url = reverse('create-campus-event', args=[str(self.campus.id)])
        self.data = {
                    'name': 'TestName',
                    'date_start': '2019-04-14',
                    'date_end': '2019-04-15',
                    'http_link': ''}

    def test_create_campus_event(self):
        self.assertEqual(len(self.campus.events), 0)
        response = self.client.post(self.url, self.data)
        body = json.loads(response.content)
        self.assertEqual(body['success'], True)
        self.assertEqual(len(self.campus.events), 1)

    def test_create_campus_empty_name(self):
        self.data['name'] = ''
        self.client.post(self.url, self.data)
        self.assertEqual(len(self.campus.events), 0)

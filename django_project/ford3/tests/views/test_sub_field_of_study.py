import json
from django.test import TestCase
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories


class TestSubFieldOfStudy(TestCase):
    def setUp(self):
        self.sfos = ModelFactories.get_sub_field_of_study_test_object()
        self.url = reverse(
            'list-sfos',
            args=[str(self.sfos.field_of_study.id)])

    def runTest(self):
        response = self.client.get(self.url)
        body = json.loads(response.content)
        self.assertEqual(
            body['results'][0]['name'],
            self.sfos.name)

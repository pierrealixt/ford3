from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestQualificationEvent(TestCase):

    def test_qualification_event_description(self):
        new_qualification_event = ModelFactories.get_qualification_event_test_object()
        self.assertEqual(new_qualification_event.__str__(), 'Qualification Event Test Name')

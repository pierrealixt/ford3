from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestCampusEvent(TestCase):

    def test_campus_event_description(self):
        new_campus_event = ModelFactories.get_campus_event_test_object()
        self.assertEqual(new_campus_event.__str__(), 'Campus Event Test Name')

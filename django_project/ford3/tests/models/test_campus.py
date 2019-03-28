from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestCampus(TestCase):

    def test_campus_description(self):
        new_campus = ModelFactories.get_campus_test_object(1)
        self.assertEqual(new_campus.__str__(), 'Object Test Name')

    def test_save_details_form_data(self):
        """
        Test saving the first form of the Campus wizard: details
        """
        self.provider = ModelFactories.get_provider_test_object(
            new_id=42)

        self.campus = ModelFactories.get_campus_test_object(
            new_id=420)

        details_form_data = {
            'telephone': '0606551967',
            'email': 'email@kartoza.com',
            'max_students_per_year': 1042
        }

        self.campus.save_form_data(details_form_data)

        self.assertEqual(self.campus.telephone, '0606551967')
        self.assertEqual(self.campus.email, 'email@kartoza.com')
        self.assertEqual(self.campus.max_students_per_year, 1042)

    def test_save_location_form_data(self):
        pass

    def test_save_dates_form_data(self):
        pass

    def test_save_qualifications(self):
        form_data = {
            'saqa_ids': '59731 90736'
        }

        self.campus.save_qualifications(form_data)

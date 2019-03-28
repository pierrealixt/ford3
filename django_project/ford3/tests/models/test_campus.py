from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.qualification import Qualification
from ford3.models.saqa_qualification import SAQAQualification


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
        campus = ModelFactories.get_campus_test_object(
            new_id=420)

        # create two SAQA Qualifications
        saqas = [
            ModelFactories.get_saqa_qualification_test_object(),
            SAQAQualification.objects.create(
                name='Hello World',
                nqf_level='42',
                saqa_id=42,
                sub_field_of_study=(
                    ModelFactories.get_sub_field_of_study_test_object(
                        new_id=42)),
            )
        ]

        # build form data
        form_data = {
            'saqa_ids': '{} {}'.format(saqas[0].saqa_id, saqas[1].saqa_id)
        }

        # campus should not have qualifications yet.
        campus_qualifications = Qualification.objects.filter(
            campus__id=campus.id)
        self.assertQuerysetEqual(campus_qualifications, [])

        # save qualifications
        campus.save_qualifications(form_data)

        # campus should have 2 qualifications.
        campus_qualifications = Qualification.objects.filter(
            campus__id=campus.id).order_by('id')
        self.assertEqual(len(campus_qualifications), 2)

        for i in range(2):
            self.assertEqual(
                campus_qualifications[i].saqa_qualification.saqa_id,
                saqas[i].saqa_id)

            self.assertEqual(
                campus_qualifications[i].saqa_qualification.name,
                saqas[i].name)

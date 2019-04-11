from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.saqa_qualification import SAQAQualification


class TestCampus(TestCase):

    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object(
            new_id=420)

    def test_campus_description(self):
        # new_campus = ModelFactories.get_campus_test_object(1)
        self.assertEqual(self.campus.__str__(), 'Object Test Name campus')

    def test_save_details_form_data(self):
        """
        Test saving the first form of the Campus wizard: details
        """
        self.provider = ModelFactories.get_provider_test_object(
            new_id=42)

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
        # form_data = {
        #     'physical_address_street_name': 'street name',
        #     'physical_address_city': 'gournay',
        #     'physical_address_postal_code': '93460',
        #     'is_physical_addr_same_as_postal_addr': True
        # }
        pass

    def test_save_events_form_data(self):

        campus_events = [ModelFactories.get_campus_event_test_object()]

        # campus should not have events yet.
        self.assertQuerysetEqual(self.campus.events, [])

        # save events
        self.campus.save_events(campus_events)

        # campus should have one event
        self.assertEqual(len(self.campus.events), 1)

    def test_save_single_event(self):
        self.assertEqual(len(self.campus.events), 0)
        campus_events = [ModelFactories.get_campus_event_test_object()]
        self.campus.save_events(campus_events)
        self.assertEqual(len(self.campus.events), 1)

    def test_save_qualifications(self):

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
        self.assertQuerysetEqual(self.campus.qualifications, [])

        # save qualifications
        self.campus.save_qualifications(form_data)

        # campus should have 2 qualifications.
        self.assertEqual(len(self.campus.qualifications), 2)

    def test_save_qualifications_duplicate(self):
        """ It should not save a duplicate qualification.
        """

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
            'saqa_ids': '{}'.format(saqas[0].saqa_id)
        }
        # save two times with same saqa_ids
        self.campus.save_qualifications(form_data)
        self.campus.save_qualifications(form_data)

        self.assertEqual(len(self.campus.qualifications), 1)

        form_data = {
            'saqa_ids': '{} {}'.format(saqas[0].saqa_id, saqas[1].saqa_id)
        }

        # save with a new saqa_id
        self.campus.save_qualifications(form_data)

        self.assertEqual(len(self.campus.qualifications), 2)

    def test_delete_qualifications(self):
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
        self.campus.save_qualifications(form_data)
        self.assertEqual(len(self.campus.qualifications), 2)

        form_data = {
            'saqa_ids': '{}'.format(saqas[1].saqa_id)
        }

        # it should remove the first saqa
        self.campus.delete_qualifications(form_data)

        self.assertEqual(len(self.campus.qualifications), 1)
        self.assertEqual(
            self.campus.qualifications[0]['saqa_qualification__saqa_id'],
            42)

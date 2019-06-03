from django.test import TestCase
from django.core.exceptions import ValidationError
from ford3.models.campus import Campus
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.user import User
from ford3.tests.models.model_factories import ModelFactories


class TestCampus(TestCase):
    fixtures = [
        'groups',
        'sa_provinces',
        'test_province_users',
        'test_provider_users',
        'test_campus_users']

    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object(
            new_id=420)
        self.user = User.objects.get(pk=3)

    def test_campus_description(self):
        # new_campus = ModelFactories.get_campus_test_object(1)
        self.assertEqual(self.campus.__str__(), 'Object Test Name')

    def test_save_details_form_data(self):
        """
        Test saving the first form of the Campus wizard: details
        """
        details_form_data = {
            'telephone': '0606551967',
            'email': 'email@kartoza.com',
            'max_students_per_year': 1042
        }

        self.campus.save_form_data(details_form_data)

        self.assertEqual(self.campus.telephone, '0606551967')
        self.assertEqual(self.campus.email, 'email@kartoza.com')
        self.assertEqual(self.campus.max_students_per_year, 1042)

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
            'saqa_ids': '{} {}'.format(saqas[0].id, saqas[1].id)
        }

        # campus should not have qualifications yet.
        self.assertQuerysetEqual(self.campus.qualifications, [])

        # save qualifications
        self.campus.save_qualifications(form_data, self.user)

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
            'saqa_ids': '{}'.format(saqas[0].id)
        }
        # save two times with same saqa_ids
        self.campus.save_qualifications(form_data, self.user)
        self.campus.save_qualifications(form_data, self.user)

        self.assertEqual(len(self.campus.qualifications), 1)

        form_data = {
            'saqa_ids': '{} {}'.format(saqas[0].id, saqas[1].id)
        }

        # save with a new saqa_id
        self.campus.save_qualifications(form_data, self.user)

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
            'saqa_ids': '{} {}'.format(saqas[0].id, saqas[1].id)
        }
        self.campus.save_qualifications(form_data, self.user)
        self.assertEqual(len(self.campus.qualifications), 2)

        # add those two qualifications to another campus
        self.other_campus = ModelFactories.get_campus_test_object(
            new_id=421)
        self.other_campus.save_qualifications(form_data, self.user)

        form_data = {
            'saqa_ids': '{}'.format(saqas[1].id)
        }

        # it should remove the first saqa for the first campus.
        self.campus.delete_qualifications(form_data)

        self.assertEqual(len(self.campus.qualifications), 1)
        self.assertEqual(
            self.campus.qualifications[0]['saqa_qualification__saqa_id'],
            42)

        # it should not remove qualifications for the second campus.
        self.assertEqual(len(self.other_campus.qualifications), 2)


class TestCreateCampus(TestCase):
    def test_create_empty_campus(self):
        with self.assertRaisesMessage(ValidationError, 'Name is required'):
            campus = Campus()
            campus.save()


    def test_create_duplicate_campus(self):
        provider = ModelFactories.get_provider_test_object()

        campus = Campus(
            name='My Campus',
            provider=provider)
        campus.save()

        with self.assertRaisesMessage(
            ValidationError,
            'Name is already taken'):
            campus_2 = Campus(
                name='My Campus',
                provider=provider)
            campus_2.save()

        provider_2 = ModelFactories.get_provider_test_object()
        campus_3 = Campus(
            name='My Campus',
            provider=provider_2)
        campus_3.save()

        self.assertEqual(campus.name, 'My Campus')
        self.assertEqual(campus_3.name, 'My Campus')

        with self.assertRaisesMessage(
            ValidationError,
            'Name is already taken'):
            campus_4 = Campus(
                name='my campus',
                provider=provider)
            campus_4.save()

    def test_create_campus(self):
        provider = ModelFactories.get_provider_test_object()

        provider.campus_set.create(
            name='My Campus')

        self.assertEqual(Campus.objects.count(), 1)

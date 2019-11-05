import os
import unittest
from tempfile import NamedTemporaryFile
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from ford3.smart_excel.smart_excel import SmartExcel
from ford3.smart_excel.definition import OPENEDU_EXCEL_DEFINITION
from ford3.views import provider as providerView
from ford3.tests.models.model_factories import ModelFactories
from ford3.models import (
    Campus,
    QualificationEntranceRequirementSubject,
    Interest
)

from ford3.import_qualifications import import_excel_data

DUMMY_DEFINITION = [
    {
        'func': 'add_group_column',
        'kwargs': {
            'columns': [
                {
                    'name': 'NAME',
                    'key': 'name',
                    'validations': {
                        'excel': {
                            'validate': 'length',
                            'criteria': '>=',
                            'value': 0,
                            'input_title': 'Your name:'
                        }
                    }
                },
                {
                    'name': 'AGE',
                    'key': 'age',
                    'validations': {
                        'list_source_func': 'get_age_list'
                    }
                },
                {
                    'name': 'CITY OF BIRTH',
                    'key': 'city',
                    'validations': {
                        'list_source_func': 'get_city_list'
                    }
                }
            ]
        }
    }
]


class Dummy():
    def __init__(self, data):
        self.name = data['name']
        self.age = data['age']
        self.city = data['city']


class DummyData():
    def __init__(self):
        self.results = [
            Dummy({
                'name': 'PA',
                'age': 29,
                'city': 'Paris'
            }),
            Dummy({
                'name': 'Cairo',
                'age': 0,
                'city': 'Muizenberg'
            }),
            Dummy({
                'name': 'Carina',
                'age': 26,
                'city': 'Windhoek'
            })
        ]


    def write_name(self, instance, kwargs={}):
        return instance.name

    def write_age(self, instance, kwargs={}):
        return instance.age

    def write_city(self, instance, kwargs={}):
        return instance.city

    def get_age_list(self):
        return [i for i in range(0, 99)]

    def get_city_list(self):
        return [
            'Paris',
            'Muizenberg',
            'Windhoek',
            'Saint-Dizier'
        ]


class TestSmartExcelDump(unittest.TestCase):
    def setUp(self):
        self.definition = DUMMY_DEFINITION
        self.data = DummyData()
        self.filepath = 'hello.xlsx'
        # /tmp/dummy_test.xlsx'

        if os.path.exists(self.filepath):
            os.remove(self.filepath)


    def runTest(self):
        self.assertFalse(os.path.exists(self.filepath))
        excel = SmartExcel(
            definition=self.definition,
            data=self.data,
            output=self.filepath
        )
        excel.dump()
        self.assertTrue(os.path.exists(self.filepath))
        self.assertTrue(excel.WRITEMODE)


class TestSmartExcelParse(unittest.TestCase):
    def setUp(self):
        self.definition = DUMMY_DEFINITION
        self.data = DummyData()
        self.filepath = '/tmp/dummy_test.xlsx'

        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        SmartExcel(
            definition=self.definition,
            data=self.data,
            output=self.filepath
        ).dump()

    def test_parse(self):
        excel = SmartExcel(
            definition=self.definition,
            data=self.data,
            path=self.filepath
        )
        data = excel.parse()

        self.assertEqual(data, [
            {'name': 'PA', 'age': 29, 'city': 'Paris'},
            {'name': 'Cairo', 'age': 0, 'city': 'Muizenberg'},
            {'name': 'Carina', 'age': 26, 'city': 'Windhoek'}])


class TestSmartExcelParseProviderSheet(TestCase):
    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object()
        self.campus = ModelFactories.get_campus_test_object()
        self.qualification = ModelFactories.get_qualification_test_object()
        self.qualification.campus_id = self.campus
        self.campus.provider_id = self.provider
        self.campus.save()
        self.requirement_subject = ModelFactories.get_qualification_entrance_requirement_to()
        self.requirement_subject.qualification = self.qualification
        self.requirement_subject.save()
        self.qualification.save()

        output_data = providerView.excel_dump(self.provider.id)
        named_tempfile = NamedTemporaryFile(suffix='.xlsx')

        with open(named_tempfile.name, 'wb') as file:
            file.write(output_data)

        excel = SmartExcel(
            definition=OPENEDU_EXCEL_DEFINITION,
            data=DummyData(),
            path=named_tempfile.name
        )
        # provider.dump(None, provider.id)
        self.data = excel.parse()

    def test_basic_parse(self):
        original_name = self.qualification.name
        self.campus.name = "Something else"
        self.campus.save()

        self.assertNotEqual(self.campus.name, original_name)

        success, errors = import_excel_data(self.data)
        self.assertTrue(success)
        self.assertIsNone(errors)

        self.campus = Campus.objects.get(pk=self.campus.id)
        self.assertEqual(original_name, self.campus.name)

    def test_alter_subject(self):
        original_required_score = self.qualification.entrance_req_subjects_list[0]['minimum_score']
        entrance_req_id = self.qualification.entrance_req_subjects_list[0]['id']
        qualification_entrance_subject = QualificationEntranceRequirementSubject.objects.get(pk=entrance_req_id)
        qualification_entrance_subject.minimum_score = 1
        qualification_entrance_subject.save()

        self.assertNotEqual(qualification_entrance_subject.minimum_score, original_required_score)

        success, errors = import_excel_data(self.data)

        self.assertTrue(success)
        self.assertIsNone(errors)

        qualification_entrance_subject = QualificationEntranceRequirementSubject.objects.get(pk=entrance_req_id)

        self.assertEqual(qualification_entrance_subject.minimum_score, original_required_score)

    def test_add_subject(self):
        original_required_score = self.qualification.entrance_req_subjects_list[0]['minimum_score']
        entrance_req_id = self.qualification.entrance_req_subjects_list[0]['id']
        QualificationEntranceRequirementSubject.objects.get(pk=entrance_req_id).delete()
        try:
            QualificationEntranceRequirementSubject.objects.get(pk=entrance_req_id)
            self.fail('Object not deleted correctly')
        except ObjectDoesNotExist:
            pass

        subject_name = ModelFactories.get_subject_test_object().name

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'qualification_entrance_requirement_subject__subject': subject_name,
            'qualification_entrance_requirement_subject__minimum_score': '42'
        }

        success, errors, diffs = import_excel_data(row)

        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertEqual(
            diffs,
            {
                'qualification_entrance_requirement_subject__minimum_score': {
                    'new': '42',
                    'old': None
                }
            }
        )

        qualification_entrance_subject = self.qualification.entrance_req_subjects_list[0]

        self.assertEqual(qualification_entrance_subject['name'], subject_name)
        self.assertEqual(qualification_entrance_subject['minimum_score'], 42)

    def test_add_subject_failed(self):
        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'qualification_entrance_requirement_subject__subject': 'Penbra History',
            'qualification_entrance_requirement_subject__minimum_score': '42'
        }

        success, errors = import_excel_data(row)

        self.assertFalse(success)

        self.assertEqual(
            errors,
            {
                'qualification_entrance_requirement_subject__subject-0': 'The subject Penbra History does not exist.'
            }
        )


    def test_add_interest(self):
        original_interest = self.qualification.interests.all()[0]
        self.assertEqual(len(self.qualification.interests.all()), 1)
        self.qualification.interests.clear()
        self.assertEqual(len(self.qualification.interests.all()), 0)

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'interest__name': self.data[0]['interest__name']
        }

        success, errors, diffs = import_excel_data(row)

        self.assertIsNone(errors)
        self.assertTrue(success)
        self.assertEqual(diffs, {})


        interest = self.qualification.interests.all()[0]
        self.assertEqual(interest.id, original_interest.id)

    def test_add_interest_failed(self):
        self.assertEqual(len(self.qualification.interests.all()), 1)
        self.qualification.interests.clear()
        self.assertEqual(len(self.qualification.interests.all()), 0)

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'interest__name': 'penbra hunting'
        }

        success, errors = import_excel_data(row)

        self.assertEqual(
            errors,
            {
                'interest__name-0': 'The interest penbra hunting does not exist.'
            }
        )
        self.assertFalse(success)

    def test_add_occupation(self):
        # todo: change that test, similar to interest
        original_occupation = self.qualification.occupations.all()[0]
        self.assertEqual(len(self.qualification.occupations.all()), 1)
        self.qualification.occupations.clear()
        self.assertEqual(len(self.qualification.occupations.all()), 0)

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'occupation__name': original_occupation.name
        }

        success, errors, diffs = import_excel_data(row)
        self.assertTrue(success)
        self.assertIsNone(errors)

        self.assertEqual(diffs, {})

        occupation = self.qualification.occupations.all()[0]
        self.assertEqual(occupation.id, original_occupation.id)

    def test_add_occupation_failed(self):
        pass
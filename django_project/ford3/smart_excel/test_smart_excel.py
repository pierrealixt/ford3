import os
import unittest
from tempfile import NamedTemporaryFile
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from ford3.smart_excel.smart_excel import SmartExcel
from ford3.smart_excel.definition import OPENEDU_EXCEL_DEFINITION
from ford3.smart_excel.data_model import OpenEduSmartExcelData
from ford3.views import provider as providerView
from ford3.tests.models.model_factories import ModelFactories
from ford3.models import (
    QualificationEntranceRequirementSubject,
    Interest,
    Subject,
    Occupation
)
from ford3.excel_importer import (
    update_qualification
)

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

    def write_get_repeat_func(self):
        return len(self.results)

    def write_get_name_func(self, instance, kwargs={}):
        return self.results[kwargs['index']].name


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
    fixtures = ['subject', 'occupation', 'interest', 'people_groups']

    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object()
        self.provider = self.campus.provider

        self.requirement_subject = ModelFactories.get_qualification_entrance_requirement_to()  # noqa
        self.qualification = self.requirement_subject.qualification

        self.qualification.campus = self.campus
        self.qualification.provider = self.provider
        self.qualification.save()

        output_data = providerView.excel_dump(self.provider.id)
        named_tempfile = NamedTemporaryFile(suffix='.xlsx')

        with open(named_tempfile.name, 'wb') as file:
            file.write(output_data)

        excel = SmartExcel(
            definition=OPENEDU_EXCEL_DEFINITION,
            data=OpenEduSmartExcelData(
                provider_id=self.provider.id
            ),
            path=named_tempfile.name
        )
        # provider.dump(None, provider.id)
        self.data = excel.parse()

    def test_total_cost(self):
        row = self.data[0]
        row['qualification__total_cost'] = 42

        success, diffs, _ = update_qualification(row)

        self.assertTrue(success)
        self.assertEqual(
            diffs['qualification__total_cost'],
            {
                'name': 'total_cost',
                'old': 'R 100000',
                'new': 'R 42'
            })


    def test_add_subject(self):
        entrance_req_id = self.qualification.entrance_req_subjects_list[0]['id']  # noqa
        QualificationEntranceRequirementSubject.objects.get(
            pk=entrance_req_id).delete()
        try:
            QualificationEntranceRequirementSubject.objects.get(
                pk=entrance_req_id)

            self.fail('Object not deleted correctly')
        except ObjectDoesNotExist:
            pass

        subject_1 = Subject.objects.get(name='English')
        subject_2 = Subject.objects.get(name='Afrikaans')

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'qualification_entrance_requirement_subject__subject': f'{subject_1.name} ({subject_1.id})',  # noqa
            'qualification_entrance_requirement_subject__minimum_score': '42',
            'qualification_entrance_requirement_subject__subject--1': f'{subject_2.name} ({subject_2.id})',  # noqa
            'qualification_entrance_requirement_subject__minimum_score--1': '42',  # noqa
            'qualification_entrance_requirement_subject__subject--2': None,
            'qualification_entrance_requirement_subject__minimum_score--2': None,  # noqa
            'qualification_entrance_requirement_subject__subject--3': None,
            'qualification_entrance_requirement_subject__minimum_score--3': None,  # noqa
            'qualification_entrance_requirement_subject__subject--4': None,
            'qualification_entrance_requirement_subject__minimum_score--4': None,  # noqa
            'qualification_entrance_requirement_subject__subject--5': None,
            'qualification_entrance_requirement_subject__minimum_score--5': None,  # noqa
        }

        success, diffs, _ = update_qualification(row)

        self.assertTrue(success)
        self.assertEqual(
            diffs['qualification_entrance_requirement_subject__subject'],
            {
                'old': None,
                'new': f'English ({subject_1.id})'
            }
        )
        self.assertEqual(
            diffs['qualification_entrance_requirement_subject__minimum_score'],
            {
                'old': None,
                'new': '42'
            }
        )

        self.assertEqual(
            diffs['qualification_entrance_requirement_subject__subject--1'],
            {
                'old': None,
                'new': f'Afrikaans ({subject_2.id})'
            }
        )
        self.assertEqual(
            diffs['qualification_entrance_requirement_subject__minimum_score--1'],  # noqa
            {
                'old': None,
                'new': '42'
            }
        )

        qualification_entrance_subject_1 = self.qualification.entrance_req_subjects_list[0]  # noqa

        self.assertEqual(qualification_entrance_subject_1['name'], subject_1.name)  # noqa
        self.assertEqual(qualification_entrance_subject_1['minimum_score'], 42)

        qualification_entrance_subject_2 = self.qualification.entrance_req_subjects_list[1]  # noqa

        self.assertEqual(qualification_entrance_subject_2['name'], subject_2.name)  # noqa
        self.assertEqual(qualification_entrance_subject_2['minimum_score'], 42)

    def test_add_interest(self):
        # original_interest = self.qualification.interests.all()[0]
        int_1 = Interest.objects.get(name='Health')
        self.assertEqual(len(self.qualification.interests.all()), 1)
        self.qualification.interests.clear()
        self.assertEqual(len(self.qualification.interests.all()), 0)

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'interest__name': int_1.name,
            'interest__name--1': None,
            'interest__name--2': None,
        }

        success, diffs, _ = update_qualification(row)

        self.assertTrue(success)
        self.assertEqual(diffs['interest__name'], {
            'old': None,
            'new': int_1.name
        })


        interest = self.qualification.interests.all()[0]
        self.assertEqual(interest.id, int_1.id)

    def test_add_occupation(self):
        # todo: change that test, similar to interest
        # original_occupation = self.qualification.occupations.all()[0]
        occ_1 = Occupation.objects.get(name='Abrasive Wheel Maker')
        self.assertEqual(len(self.qualification.occupations.all()), 1)
        self.qualification.occupations.clear()
        self.assertEqual(len(self.qualification.occupations.all()), 0)

        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'occupation__name': occ_1.name,
            'occupation__name--1': 'prout',
            'occupation__name--2': None,
            'occupation__name--3': None,
            'occupation__name--4': None
        }

        success, diffs, _ = update_qualification(row)
        self.assertTrue(success)

        self.assertEqual(diffs['occupation__name'], {
            'new': 'Abrasive Wheel Maker',
            'old': None
        })

        occupation = self.qualification.occupations.all()[0]
        self.assertEqual(occupation.id, occ_1.id)

    def test_update_aps(self):
        row = {
            'qualification__id': self.data[0]['qualification__id'],
            'admission_point_score__value': 0,
            'admission_point_score__value--1': 2,
        }

        success, diffs, _ = update_qualification(row)

        self.assertEqual(
            diffs['admission_point_score__value'],
            {
                'old': None,
                'new': 0
            }
        )

        self.assertEqual(
            diffs['admission_point_score__value--1'],
            {
                'old': None,
                'new': 2
            }
        )

        self.assertEqual(
            self.qualification.requirement.admission_point_scores[0]['value'],
            0)

        self.assertEqual(
            self.qualification.requirement.admission_point_scores[1]['value'],
            2)

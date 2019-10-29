import os
import io
import unittest
from tempfile import NamedTemporaryFile
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from json import dumps
from ford3.smart_excel.smart_excel import SmartExcel
from ford3.smart_excel.definition import OPENEDU_EXCEL_DEFINITION
from ford3.views import provider
from ford3.tests.models.model_factories import ModelFactories
from ford3.models import Campus
from ford3.models import Qualification
from ford3.models import QualificationEntranceRequirementSubject


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

        output_data = provider.excel_dump(self.provider.id)
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

        # path = '{base_path}/ford3/tests/data_test/template.xlsx'.format(base_path=settings.DJANGO_PATH)



        original_name = self.qualification.name
        self.campus.name = "Something else"
        self.campus.save()

        self.assertNotEqual(self.campus.name, original_name)

        self.provider.import_excel_data(self.data)
        self.campus = Campus.objects.get(pk=self.campus.id)
        self.assertEqual(original_name, self.campus.name)

    def test_alter_subject(self):
        original_required_score = self.qualification.entrance_req_subjects_list[0]['minimum_score']
        entrance_req_id = self.qualification.entrance_req_subjects_list[0]['id']
        qualification_entrance_subject = QualificationEntranceRequirementSubject.objects.get(pk=entrance_req_id)
        qualification_entrance_subject.minimum_score = 1
        qualification_entrance_subject.save()
        self.assertNotEqual(qualification_entrance_subject.minimum_score, original_required_score)
        self.provider.import_excel_data(self.data)
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

        self.provider.import_excel_data(self.data)
        qualification_entrance_subject = self.qualification.entrance_req_subjects_list[0]
        self.assertEqual(qualification_entrance_subject['minimum_score'], original_required_score)

# class TestSmartExcel(TestCase):
#     fixtures = ['interest', 'occupation', 'subject', 'groups',
#         'sa_provinces',
#         'test_province_users',
#         'test_provider_users',
#         'test_campus_users',
# 'test_providers', 'test_campus', 'test_qualification']

#     def setUp(self):
#         qualif = Qualification.objects.all()[0]
#         for occ in Occupation.objects.all()[0:5]:
#             qualif.occupations.add(occ)

#         for inte in Interest.objects.all()[0:3]:
#             qualif.interests.add(inte)

#         for sub in Subject.objects.all()[0:6]:
#             cairo = QualificationEntranceRequirementSubject(
#                 qualification=qualif,
#                 subject=sub,
#                 minimum_score=42
#             )
#             cairo.save()
#         from ford3.models.requirement import Requirement
#         from ford3.enums.saqa_qualification_level import SaqaQualificationLevel

#         requirememt = Requirement()
#         requirememt.qualification = qualif
#         requirememt.min_nqf_level = SaqaQualificationLevel.LEVEL_3
#         requirememt.save()


#         qualif = Qualification.objects.all()[1]
#         for occ in Occupation.objects.all()[5:10]:
#             qualif.occupations.add(occ)

#         for inte in Interest.objects.all()[3:6]:
#             qualif.interests.add(inte)

#         for sub in Subject.objects.all()[6:12]:
#             cairo = QualificationEntranceRequirementSubject(
#                 qualification=qualif,
#                 subject=sub,
#                 minimum_score=42
#             )
#             cairo.save()

#         self.excel = SmartExcel()
#         self.excel.data = OpenEduSmartExcelData(provider_id=1)

#         OpenEduSmartExcel(self.excel)


#     def test_next_letter(self):
#         from ford3.tests.smart_excel.smart_excel import next_letter
#         letter = next_letter(0)
#         self.assertEqual(letter, 'A')

#         letter = next_letter(1)
#         self.assertEqual(letter, 'B')

#         letter = next_letter(26)
#         self.assertEqual(letter, 'AA')

#         letter = next_letter(27)
#         self.assertEqual(letter, 'AB')

#         letter = next_letter(51)
#         self.assertEqual(letter, 'AZ')

#         letter = next_letter(52)
#         self.assertEqual(letter, 'BA')

#         letter = next_letter(53)
#         self.assertEqual(letter, 'BB')

#         letter = next_letter(78)
#         self.assertEqual(letter, 'CA')

#         letter = next_letter(701)
#         self.assertEqual(letter, 'ZZ')

#         letter = next_letter(702)
#         self.assertEqual(letter, 'AAA')

#         letter = next_letter(703)
#         self.assertEqual(letter, 'AAB')

#     def test_build(self):
#         self.excel.build()

#     def test_dump(self):
#         self.excel.dump()

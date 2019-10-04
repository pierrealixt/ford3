import os
from django.test import TestCase
from ford3.smart_excel.open_edu_smart_excel import (
    OPENEDU_EXCEL_DEFINITION,
    OpenEduSmartExcelData
)
from ford3.smart_excel.smart_excel import SmartExcel

VALID_XLSX = 'data_test/template.xlsx'

class TestParseExcel(TestCase):
    fixtures = ['interest', 'occupation', 'subject', 'groups',
        'sa_provinces',
        'test_province_users',
        'test_provider_users',
        'test_campus_users',
'test_providers', 'test_campus', 'test_qualification']

    def setUp(self):
        pass

    def runTest(self):

        provider_id = 1

        # path = '{dir_path}/{filename}'.format(
        #     dir_path=os.path.dirname(os.path.realpath(__file__)),
        #     filename=VALID_XLSX
        # )

        self.excel_one = SmartExcel(
            definition=OPENEDU_EXCEL_DEFINITION,
            data=OpenEduSmartExcelData(provider_id)
        )

        self.excel_one.dump()

        self.excel = SmartExcel(
            definition=OPENEDU_EXCEL_DEFINITION,
            data=OpenEduSmartExcelData(provider_id),
            path='template.xlsx',
        )

        self.excel.parse()


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
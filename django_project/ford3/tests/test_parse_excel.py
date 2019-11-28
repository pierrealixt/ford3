from django.test import TestCase
from ford3.smart_excel.definition import OPENEDU_EXCEL_DEFINITION
from ford3.smart_excel.data_model import OpenEduSmartExcelData
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

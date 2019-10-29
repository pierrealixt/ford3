from django.core.management.base import BaseCommand
from ford3.smart_excel.smart_excel import SmartExcel
from ford3.smart_excel.definition import OPENEDU_EXCEL_DEFINITION
from ford3.smart_excel.data_model import OpenEduSmartExcelData

class Command(BaseCommand):
    def handle(self, *args, **options):

        provider_id = 96

        self.excel = SmartExcel(
            definition=OPENEDU_EXCEL_DEFINITION,
            data=OpenEduSmartExcelData(provider_id)
        )
        self.excel.dump()

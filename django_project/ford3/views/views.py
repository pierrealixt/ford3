# coding=utf-8

from django.conf import settings
from formtools.wizard.views import CookieWizardView


class CampusWizard(CookieWizardView):

    file_storage = settings.DEFAULT_FILE_STORAGE

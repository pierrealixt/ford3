from django.views.generic import TemplateView
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView


class QualificationFormView(SessionWizardView):
    def done(self, form_list, **kwargs):
        return redirect('/')

from django.shortcuts import redirect
from formtools.wizard.views import NamedUrlSessionWizardView


class QualificationFormWizard(NamedUrlSessionWizardView):
    template_name = 'qualification_form.html'

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Duration & Fees'
        ]
        return context

    def done(self, form_list, **kwargs):
        return redirect('/')

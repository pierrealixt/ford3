from django.shortcuts import Http404, get_object_or_404
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Campus
)


class CampusFormWizard(CookieWizardView):

    template_name = 'campus_form.html'

    @property
    def campus(self):
        campus_id = self.kwargs['campus_id']
        return get_object_or_404(
            Campus,
            id=campus_id)

    def get(self, *args, **kwargs):
        if not self.campus:
            raise Http404()
        return super(CampusFormWizard, self).get(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Location',
            'Important Dates',
            'Qualification Titles'
        ]
        context['campus'] = self.campus
        return context

    def done(self, form_list, **kwargs):
        pass

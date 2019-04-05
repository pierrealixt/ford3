import os
from django.shortcuts import redirect, Http404, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Campus,
    Provider
)


class CampusFormWizard(CookieWizardView):

    template_name = 'campus_form.html'
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    @property
    def campus(self):
        campus_id = self.kwargs['campus_id']
        return get_object_or_404(
            Campus,
            id=campus_id)

    @property
    def provider(self):
        provider_id = self.kwargs['provider_id']
        return get_object_or_404(
            Provider,
            id=provider_id)

    def get(self, *args, **kwargs):
        if not self.campus or not self.provider:
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
        context['provider'] = self.provider

        return context

    def done(self, form_list, **kwargs):
        steps = {
            'DETAILS': 0,
            'LOCATION': 1,
            'DATES': 2,
            'QUALIFICATION_TITLES': 3
        }

        i = 0
        for form in form_list:
            if i == steps['DETAILS'] or i == steps['LOCATION']:
                self.campus.save_form_data(form.cleaned_data)
            elif i == steps['DATES']:
                print(form.cleaned_data)
                self.campus.save_events(form.cleaned_data)
            elif i == steps['QUALIFICATION_TITLES']:
                self.campus.save_qualifications(form.cleaned_data)
            i += 1

        url = reverse('show-campus', args=(self.provider.id, self.campus.id))
        return redirect(url)

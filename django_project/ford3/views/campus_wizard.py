import os
from django.shortcuts import Http404, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
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

        if self.steps.current == '3':
            context.update({'saqa_qualifications': [
                {
                    'saqa_id': 1000,
                    'name': 'Bachelor in Art',
                    'field_of_study': 'Arts',
                    'subfield_of_study': '...'
                },
                {
                    'saqa_id': 1001,
                    'name': 'Bachelor in Computer Science',
                    'field_of_study': 'Technology',
                    'subfield_of_study': '...'
                },
            ]})
        return context

    def done(self, form_list, **kwargs):
        for form in form_list:
            print(form.cleaned_data)

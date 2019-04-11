import os
from datetime import datetime
from django.shortcuts import redirect, Http404, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.forms.models import model_to_dict
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Campus,
    CampusEvent,
    Provider
)


class CampusFormWizard(CookieWizardView):
    template_name = 'campus_form.html'
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    new_campus_events = []

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

    def get_form_initial(self, step):
        # For 'Details' and 'Location' forms
        initial_dict = model_to_dict(self.campus)

        # For 'Qualification Titles' form
        saqa_ids = ' '.join([
            str(s['saqa_qualification__saqa_id'])
            for s in self.campus.qualifications])

        initial_dict.update({'saqa_ids': saqa_ids})
        return initial_dict

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
                self.campus.save_events(self.new_campus_events)
            elif i == steps['QUALIFICATION_TITLES']:
                self.campus.save_qualifications(form.cleaned_data)
                self.campus.delete_qualifications(form.cleaned_data)
            i += 1
        url = reverse('show-campus', args=(self.provider.id, self.campus.id))
        return redirect(url)

    def add_events(self, step_data, current_form):
        new_name = step_data['campus-dates-event_name']
        new_date_start = step_data['campus-dates-date_start']
        new_date_end = step_data['campus-dates-date_end']
        new_http_link = step_data['campus-dates-http_link']
        # Count how many names were submitted and create new_events
        number_of_new_events = len(new_name)
        if len(new_name) == 1 and new_name[0] == '':
            return False
        for i in range(0, number_of_new_events):
            new_campus_event = CampusEvent()
            new_campus_event.name = new_name[i]
            new_date_start_i = new_date_start[i]
            new_date_start_formatted = (
                datetime.strptime(new_date_start_i, '%m/%d/%Y')
            ).strftime('%Y-%m-%d')
            new_date_end_i = new_date_end[i]
            new_date_end_formatted = (
                datetime.strptime(new_date_end_i, '%m/%d/%Y')
            ).strftime('%Y-%m-%d')
            new_campus_event.date_start = new_date_start_formatted
            new_campus_event.date_end = new_date_end_formatted
            new_campus_event.http_link = new_http_link[i]
            self.new_campus_events.append(new_campus_event)

    def render(self, form=None, **kwargs):
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        current_step = context['view'].storage.current_step
        step_before = 'campus-location'
        step_after = 'campus-qualifications'
        # Currently this simply clears the events forcing the user to re-enter
        # TODO: Generate events from stored self.new_campus_events
        if current_step == 'campus-dates':
            self.new_campus_events = []

        if current_step == step_before or current_step == step_after:
            try:
                self.add_events(
                    context['view'].storage.data['step_data']['campus-dates'],
                    form)
            except KeyError:
                pass
        return self.render_to_response(context)

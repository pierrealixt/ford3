import os
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, Http404, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.forms.models import model_to_dict
from django.template.defaulttags import register
from formtools.wizard.views import CookieWizardView
from ford3.views.wizard_utilities import get_form_identifier_list_from_keys
from ford3.models.campus import Campus
from ford3.models.provider import Provider
from ford3.models.field_of_study import FieldOfStudy


class CampusFormWizard(LoginRequiredMixin, CookieWizardView):
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
        if 'step' in self.request.GET and 'multi_step' not in self.request.GET:
            return super().render_goto_step(self.request.GET['step'], **kwargs)
        else:
            return super(CampusFormWizard, self).get(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Location',
            'Events',
            'Qualifications'
        ]
        context['form_identifier_list'] = (
            get_form_identifier_list_from_keys(
                self.form_list, context['form_name_list']))

        context['campus'] = self.campus
        context['provider'] = self.provider
        context['provider_logo'] = self.provider.provider_logo.url \
            if self.provider.provider_logo else ""
        form_data = {
            'provider_name': self.provider.name
        }
        context['form_data'] = form_data

        context['multi_step_form'] = True
        context['fos'] = FieldOfStudy.objects.all()

        if 'step' in self.request.GET and 'multi-step' not in self.request.GET:
            context['multi_step_form'] = False

        return context

    def get_form_initial(self, step):
        # For 'Details' and 'Location' forms
        initial_dict = model_to_dict(self.campus)

        # events
        event_ids = ' '.join([
            str(event['id'])
            for event in self.campus.events])

        # For 'Qualification Titles' form
        saqa_ids = ' '.join([
            str(s['saqa_qualification__id'])
            for s in self.campus.qualifications])

        initial_dict.update({
            'saqa_ids': saqa_ids,
            'event_ids': event_ids,
        })
        try:
            initial_dict.update({
                'location_value_x': self.campus.location.x,
                'location_value_y': self.campus.location.y})
        except (IndexError, AttributeError):
            initial_dict.update({
                'location_value_x': 0,
                'location_value_y': 0})

        return initial_dict

    def process_step(self, form):
        return self.get_form_step_data(form)

    def done(self, form_list, **kwargs):
        for form in kwargs['form_dict']:
            cleaned_data = kwargs['form_dict'][form].cleaned_data

            if form == 'campus-details':
                self.campus.save_form_data(cleaned_data)
            elif form == 'campus-location':
                self.campus.save_location_data(cleaned_data)
                self.campus.save_postal_data(cleaned_data)
            elif form == 'campus-qualifications':
                self.campus.save_qualifications(
                    cleaned_data,
                    self.request.user)
                self.campus.delete_qualifications(cleaned_data)

        Campus.objects \
            .filter(pk=self.campus.id) \
            .update(edited_by=self.request.user)

        url = reverse('show-campus', args=(self.provider.id, self.campus.id))
        return redirect(url)

    def render_next_step(self, form, **kwargs):
        """
        This method gets called when the next step/form should be rendered.
        `form` contains the last/current form.
        """
        # get the form instance based on the data from the storage backend
        # (if available).

        if 'step' in self.request.GET and 'multi-step' not in self.request.GET:
            return self.render_done(form, **kwargs)
        else:
            return super().render_next_step(form, **kwargs)

    def render_done(self, form, **kwargs):
        """
        This method gets called when all forms passed. The method should also
        re-validate all steps to prevent manipulation. If any form fails to
        validate, `render_revalidation_failure` should get called.
        If everything is fine call `done`.
        """
        final_forms = OrderedDict()

        if ('step' in self.request.GET and 'multi-step'
                not in self.request.GET and self.request.method != 'POST'):
            form_list = [self.request.GET['step']]
        else:
            form_list = self.get_form_list()

        # walk through the form list and try to validate the data again.
        for form_key in form_list:
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )

            if not form_obj.is_valid() and form_obj.is_bound:
                return self.render_revalidation_failure(
                    form_key, form_obj, **kwargs)
            if form_obj.is_valid and form_obj.is_bound:
                final_forms[form_key] = form_obj

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(
            final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()

        return done_response

    def post(self, *args, **kwargs):
        return super().post(self, *args, **kwargs)


@register.filter
def get_dictionary_item(dictionary, key):
    return dictionary.get(key)

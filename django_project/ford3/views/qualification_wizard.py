import json
import re
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, Http404, get_object_or_404
from django.urls import reverse
from django.forms.models import model_to_dict
from django.template.defaulttags import register
from django.contrib.auth.mixins import UserPassesTestMixin
from formtools.wizard.views import CookieWizardView
from ford3.views.wizard_utilities import get_form_identifier_list_from_keys
from ford3.models.qualification import Qualification
from ford3.models.requirement import Requirement
from ford3.models.subject import Subject
from ford3.models.qualification_entrance_requirement_subject import QualificationEntranceRequirementSubject # noqa
from ford3.models.provider import Provider
from ford3.models.campus import Campus
from ford3.models.admission_point_score import AdmissionPointScore
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
)
from ford3.decorators import (
    predicate_provider,
    predicate_campus,
    predicate_qualification
)


class QualificationFormWizardDataProcess(object):
    new_qualification_events = []

    def __init__(self, qualification, edited_by):
        self.qualification = qualification
        self.new_qualification_events = []
        self.edited_by = edited_by

    def duration_in_months(self, duration, duration_type):
        """
        Get duration in months
        :param duration: int of duration
        :param duration_type: duration type, month or year
        :return: duration in months
        """
        if duration_type == 'month':
            duration_in_months = duration
        else:
            # In years
            duration_in_months = 12 * duration
        return duration_in_months

    def qualification_form_data(self, form_data):
        """
        Get all qualification form fields with data
        :param form_data: form data
        :return: dict of qualification data
        """
        qualification_fields = {}
        detail_form_fields = (
            vars(QualificationDetailForm)['declared_fields']
        )
        duration_fees_form_fields = (
            vars(QualificationDurationFeesForm)['declared_fields']
        )
        interests_and_jobs_form_fields = (
            vars(QualificationInterestsAndJobsForm)['declared_fields']
        )
        qualification_form_fields = (
            list(detail_form_fields.keys()
                 ) + list(duration_fees_form_fields.keys()
                          ) + list(interests_and_jobs_form_fields.keys())
        )
        for qualification_field in qualification_form_fields:
            try:
                getattr(Qualification, qualification_field)
                qualification_fields[qualification_field] = (
                    form_data[qualification_field]
                )
            except (AttributeError, KeyError):
                continue
        return qualification_fields

    def add_or_update_subjects(self, form_data):
        """
        Add subjects to qualification
        :param form_data: dict of form data
        """
        if form_data['require_certain_subjects']:
            QualificationEntranceRequirementSubject.objects.filter(
                qualification=self.qualification).delete()

            for subject_score_tuple in form_data['subjects_scores'].split(','):
                match = re.match(r'\(([0-9]*) ([0-9]*)\)', subject_score_tuple)
                if match:
                    subject_id, minimum_score = match.groups()
                    try:
                        req_subject = QualificationEntranceRequirementSubject\
                            .objects\
                            .get(
                                subject_id=subject_id,
                                qualification_id=self.qualification.id)

                        req_subject.minimum_score = minimum_score
                        req_subject.save()

                    except QualificationEntranceRequirementSubject.DoesNotExist: # noqa
                        req_subject = QualificationEntranceRequirementSubject\
                            .objects\
                            .create(
                                qualification_id=self.qualification.id,
                                subject_id=subject_id,
                                minimum_score=minimum_score
                            )
        else:
            QualificationEntranceRequirementSubject.objects.filter(
                qualification=self.qualification).delete()

    def add_or_update_requirements(self, form_data):
        """
        Add requirements to qualification
        :param form_data: dict of form data
        """

        if 'admission_point_scores' in form_data:
            aps = form_data['admission_point_scores']
            del form_data['admission_point_scores']

        if self.qualification.requirement is not None:
            existing_requirement: Requirement = self.qualification.requirement
            existing_requirement.min_nqf_level = (
                form_data['min_nqf_level'])
            existing_requirement.interview = (
                form_data['interview'])
            existing_requirement.portfolio = (
                form_data['portfolio'])
            existing_requirement.portfolio_comment = (
                form_data['portfolio_comment'])
            existing_requirement.assessment = (
                form_data['assessment'])
            existing_requirement.assessment_comment = (
                form_data['assessment_comment'])
            existing_requirement.require_certain_subjects = (
                form_data['require_certain_subjects'])
            existing_requirement.require_aps_score = (
                form_data['require_aps_score'])
            existing_requirement.aps_calculator_link = (
                form_data['aps_calculator_link'])

            existing_requirement.save()
        else:
            requirement_fields = {}
            requirement_form_fields = (
                vars(QualificationRequirementsForm)['declared_fields']
            )
            for requirement_field in requirement_form_fields.keys():
                try:
                    getattr(Requirement, requirement_field)
                    if requirement_field in form_data:
                        requirement_fields[requirement_field] = (
                            form_data[requirement_field]
                        )
                except AttributeError:
                    continue
            if requirement_form_fields:
                Requirement.objects.create(
                    qualification=self.qualification,
                    **requirement_fields
                )
        if form_data['require_aps_score']:
            if aps:
                self.qualification.requirement.admission_point_scores = aps
        else:
            self.qualification.requirement.reset_admission_point_scores()

    def process_data(self, form_data):
        """
        Process qualification form data then update qualification
        :param form_data: dict of form data
        """

        qualification_form_data = self.qualification_form_data(
            form_data
        )

        Qualification.objects.filter(
            id=self.qualification.id
        ).update(
            **qualification_form_data,
            edited_by=self.edited_by
        )
        try:
            # Update interests
            interests = form_data['interest_list']
            for interest in self.qualification.interests.all():
                self.qualification.interests.remove(interest)
            for interest in interests:
                self.qualification.interests.add(interest)
        except KeyError:
            pass

        try:
            # Update occupations
            occupations = form_data['occupations_ids']
            self.qualification.toggle_occupations(occupations)
        except KeyError:
            pass

        try:
            # Add requirements
            self.add_or_update_requirements(form_data)
        except KeyError:
            pass

        try:
            # Add subjects
            self.add_or_update_subjects(form_data)
        except KeyError:
            pass



class QualificationFormWizard(
    UserPassesTestMixin,
    LoginRequiredMixin,
    CookieWizardView):

    template_name = 'qualification_form.html'
    initial_dict = {}

    def test_func(self):
        if self.request.user.is_authenticated:
            return predicate_provider(
                self.request.user,
                self.kwargs['provider_id']) and\
                predicate_campus(
                    self.kwargs['provider_id'],
                    self.kwargs['campus_id']) and\
                predicate_qualification(
                    self.kwargs['campus_id'],
                    self.kwargs['qualification_id'])
        else:
            return False

    def handle_no_permission(self):
        return redirect(reverse('dashboard'))

    @property
    def provider(self):
        """
        Get provider from id
        :return: provider object
        """
        provider_id = self.kwargs['provider_id']
        if not provider_id:
            raise Http404()
        return get_object_or_404(
            Provider,
            id=provider_id
        )

    @property
    def campus(self):
        """
        Get campus from id
        :return: campus object
        """
        campus_id = self.kwargs['campus_id']
        if not campus_id:
            raise Http404()
        return get_object_or_404(
            Campus,
            id=campus_id
        )

    @property
    def qualification(self):
        """
        Get qualification from id
        :return: qualification object
        """
        try:
            return self.provider.campus_set.get(
                pk=self.kwargs['campus_id']).qualification_set.get(
                    pk=self.kwargs['qualification_id'])
        except (Provider.DoesNotExist, Campus.DoesNotExist, Qualification.DoesNotExist): # noqa
            raise Http404()

    def get(self, *args, **kwargs):
        self.qualification
        if 'step' in self.request.GET:
            return super().render_goto_step(self.request.GET['step'], **kwargs)
        else:
            return super(QualificationFormWizard, self).get(*args, **kwargs)

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


    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Duration & Fees',
            'Requirements',
            'Interests & Jobs',
            'Important Dates',
        ]
        context['form_identifier_list'] = (
            get_form_identifier_list_from_keys(
                self.form_list, context['form_name_list']))
        context['qualification'] = self.qualification
        context['provider'] = self.provider
        # make sure logo has been uploaded before set the context
        # otherwise, let it empty
        context['provider_logo'] = \
            self.qualification.campus.provider.provider_logo.url \
            if self.qualification.campus.provider.provider_logo else ""

        if self.steps.current == 'qualification-requirements':
            context['subjects'] = list(Subject.objects
                .all()
                .values('id', 'name')
                .order_by('is_language', 'name'))

            if self.qualification.requirement:
                context['aps'] = json.dumps(self.qualification.requirement.admission_point_scores) # noqa
            else:
                context['aps'] = json.dumps(AdmissionPointScore.init())

        if self.steps.current == 'qualification-interests-jobs':
            context['occupations'] = self.qualification.occupations.all()

        if self.steps.current == 'qualification-important-dates':
            context['events_list'] = self.qualification.events
        context['multi_step_form'] = True
        if 'step' in self.request.GET and 'multi-step' not in self.request.GET:
            context['multi_step_form'] = False

        return context

    def get_form_initial(self, step):
        initial_dict = model_to_dict(self.qualification)
        if step == 'qualification-requirements' and\
            self.qualification.requirement is not None:
            initial_dict = model_to_dict(self.qualification.requirement)
        if step == 'qualification-interests-jobs':
            occupations_ids = ' '.join(self.qualification.occupation_ids)
            initial_dict.update({
                'occupations_ids': occupations_ids,
                'interest_list': initial_dict['interests']})
        if step == 'qualification-requirements':
            subjects_scores = ','.join([
                f'({req_subject.subject_id} {req_subject.minimum_score})'
                for req_subject in
                QualificationEntranceRequirementSubject
                .objects
                .filter(
                    qualification_id=self.qualification.id)])

            if self.qualification.requirement:
                aps_set = self.qualification.requirement.admission_point_scores
            else:
                aps_set = AdmissionPointScore.init()

            aps = ','.join([
                f"({r_aps['group']['id']} {r_aps['value']})"
                for r_aps in aps_set
            ])

            initial_dict.update({
                'subjects_scores': subjects_scores,
                'admission_point_scores': aps
            })
        return initial_dict

    def done(self, form_list, **kwargs):
        form_data = dict()
        for form in form_list:
            if form.is_bound and form.prefix != \
                    'qualification-important-dates':
                form_data.update(form.cleaned_data)

        qualification_data_process = QualificationFormWizardDataProcess(
            self.qualification,
            self.request.user
        )
        qualification_data_process.process_data(form_data)

        url = reverse(
            'show-qualification',
            args=(self.provider.id, self.campus.id, self.qualification.id))
        return redirect(url)

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
        self.qualification.save()
        return done_response


@register.filter
def get_dictionary_item(dictionary, key):
    return dictionary.get(key)

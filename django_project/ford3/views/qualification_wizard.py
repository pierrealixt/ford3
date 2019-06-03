from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, Http404, get_object_or_404
from django.urls import reverse
from django.forms.models import model_to_dict
from formtools.wizard.views import CookieWizardView
from ford3.models.qualification import Qualification
from ford3.models.requirement import Requirement
from ford3.models.subject import Subject
from ford3.models.qualification_entrance_requirement_subject import QualificationEntranceRequirementSubject # noqa
from ford3.models.provider import Provider
from ford3.models.campus import Campus
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
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
            except AttributeError:
                continue
        return qualification_fields

    def add_subjects(self, form_data):
        """
        Add subjects to qualification
        :param form_data: dict of form data
        """
        # Remove old subjects
        QualificationEntranceRequirementSubject.objects.filter(
            qualification=self.qualification).delete()
        subject_list = form_data['subject_list'].split(',')
        minimum_score_list = form_data['minimum_score_list'].split(',')
        for index, subject_value in enumerate(subject_list):
            try:
                subject = Subject.objects.get(
                    id=subject_value
                )
            except (Subject.DoesNotExist, ValueError):
                continue
            requirement_subjects, created = (
                QualificationEntranceRequirementSubject.objects.
                get_or_create(
                    subject=subject,
                    qualification=self.qualification,
                )
            )
            try:
                minimum_score_value = int(minimum_score_list[index])
            except IndexError:
                continue
            if minimum_score_value == -1:
                continue
            requirement_subjects.minimum_score = (
                minimum_score_value
            )
            requirement_subjects.save()

    def add_or_update_requirements(self, form_data):
        """
        Add requirements to qualification
        :param form_data: dict of form data
        """
        # Check if there is already a requirements object
        requirement_exists = True
        existing_requirement: Requirement = self.qualification.requirement
        try:
            existing_requirement.qualification
        except AttributeError:
            requirement_exists = False
        if requirement_exists:
            existing_requirement.min_nqf_level = (
                form_data['min_nqf_level'])
            existing_requirement.interview = (
                form_data['interview'])
            existing_requirement.portfolio = (
                form_data['portfolio'])
            existing_requirement.portfolio_comment = (
                form_data['portfolio_comment'])
            existing_requirement.require_aps_score = (
                form_data['require_aps_score'])
            existing_requirement.aps_calculator_link = (
                form_data['aps_calculator_link'])
            existing_requirement.require_certain_subjects = (
                form_data['require_certain_subjects'])
            existing_requirement.save()
        else:
            requirement_fields = {}
            requirement_form_fields = (
                vars(QualificationRequirementsForm)['declared_fields']
            )
            for requirement_field in requirement_form_fields.keys():
                try:
                    getattr(Requirement, requirement_field)
                    if form_data[requirement_field]:
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

    def process_data(self, form_data):
        """
        Process qualification form data then update qualification
        :param form_data: dict of form data
        """
        qualification_form_data = self.qualification_form_data(
            form_data
        )
        # Check duration
        if form_data['duration']:
            qualification_form_data['duration_in_months'] = (
                self.duration_in_months(
                    duration=form_data['duration'],
                    duration_type=form_data['duration_type']
                )
            )

        Qualification.objects.filter(
            id=self.qualification.id
        ).update(
            **qualification_form_data,
            edited_by=self.edited_by
        )

        # Update interests
        interests = form_data['interest_list']
        for interest in self.qualification.interests.all():
            self.qualification.interests.remove(interest)
        for interest in interests:
            self.qualification.interests.add(interest)

        # Update occupations
        occupations = form_data['occupations_ids']
        self.qualification.toggle_occupations(occupations)

        # Add requirements
        self.add_or_update_requirements(form_data)


class QualificationFormWizard(LoginRequiredMixin, CookieWizardView):
    template_name = 'qualification_form.html'
    initial_dict = {}

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
        qualification_id = self.kwargs['qualification_id']
        if not qualification_id:
            raise Http404()
        return get_object_or_404(
            Qualification,
            id=qualification_id
        )

    def get(self, *args, **kwargs):
        qualification = self.qualification
        if not qualification:
            raise Http404()
        return super(QualificationFormWizard, self).get(*args, **kwargs)

    def get_context_data(self, form, **kwargs):

        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Duration & Fees',
            'Requirements',
            'Interest & Jobs',
            'Important Dates',
        ]
        context['qualification'] = self.qualification
        context['provider'] = self.provider
        # make sure logo has been uploaded before set the context
        # otherwise, let it empty
        context['provider_logo'] = \
            self.qualification.campus.provider.provider_logo.url \
            if self.qualification.campus.provider.provider_logo else ""

        if self.steps.current == 'qualification-requirements':
            context['subjects_list'] = \
                self.qualification.entrance_req_subjects_list

        if self.steps.current == 'qualification-interets-jobs':
            context['occupations'] = self.qualification.occupations.all()

        if self.steps.current == 'qualification-dates':
            context['events_list'] = self.qualification.events

        return context

    def get_form_initial(self, step):
        initial_dict = model_to_dict(self.qualification)
        if step == 'qualification-requirements':
            initial_dict = model_to_dict(self.qualification.requirement)
        if step == 'qualification-interets-jobs':
            occupations_ids = ' '.join(self.qualification.occupation_ids)
            initial_dict.update({
                'occupations_ids': occupations_ids,
                'interest_list': initial_dict['interests']})
        return initial_dict

    def done(self, form_list, **kwargs):
        form_data = dict()
        for form in form_list:
            if form.prefix == 'qualification-requirements':
                context = self.get_context_data(form=form, **kwargs)
                self.add_required_subjects(
                    context['view'].storage.data['step_data']['qualification-requirements']) # noqa
                form_data.update(form.cleaned_data)
            else:
                form_data.update(form.cleaned_data)

        qualification_data_process = QualificationFormWizardDataProcess(
            self.qualification,
            self.request.user
        )
        qualification_data_process.process_data(
            form_data
        )

        url = reverse(
            'show-qualification',
            args=(self.provider.id, self.campus.id, self.qualification.id))
        return redirect(url)

    def add_required_subjects(self, step_data):
        # Remove old subjects
        QualificationEntranceRequirementSubject.objects.filter(
            qualification__id=self.qualification.id).delete()
        new_subject_values = step_data['2-subject']
        new_minimum_scores = step_data['2-subject-minimum-score']
        number_of_new_subjects = len(new_subject_values)
        for i in range(0, number_of_new_subjects):
            try:
                subject = Subject.objects.filter(
                    id=new_subject_values[i]).first()
                new_subject = QualificationEntranceRequirementSubject()
                new_subject.subject = subject
                new_subject.qualification = self.qualification
                new_subject.minimum_score = new_minimum_scores[i]
                new_subject.save()
            except (Subject.DoesNotExist, ValueError):
                # ToDo: I need to alert the user one of the subjects could
                #  not be saved
                pass

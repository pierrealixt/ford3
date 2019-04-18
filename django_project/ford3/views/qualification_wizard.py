from datetime import datetime
from django.shortcuts import redirect, Http404, get_object_or_404
from django.urls import reverse
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Qualification,
    Requirement,
    Subject,
    QualificationEntranceRequirementSubject,
    QualificationEvent,
    Provider,
    Campus
)
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
)


class QualificationFormWizardDataProcess(object):
    new_qualification_events = []

    def __init__(self, qualification):
        self.qualification = qualification
        self.new_qualification_events = []

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
        subject_list = form_data['subject_list'].split(',')
        minimum_score_list = form_data['minimum_score_list'].split(',')
        for index, subject_value in enumerate(subject_list):
            try:
                subject = Subject.objects.get(
                    id=subject_value
                )
            except Subject.DoesNotExist:
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

    def add_requirements(self, form_data):
        """
        Add requirements to qualification
        :param form_data: dict of form data
        """
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
            **qualification_form_data
        )

        # Update interests
        interests = form_data['interest_list']
        for interest in self.qualification.interests.all():
            self.qualification.interests.remove(interest)
        for interest in interests:
            self.qualification.interests.add(interest)

        # Update occupations
        occupations = form_data['occupation_list']
        for occupation in self.qualification.occupations.all():
            self.qualification.occupations.remove(occupation)
        for occupation in occupations:
            self.qualification.occupations.add(occupation)

        # Subjects
        self.add_subjects(form_data)

        # Add requirements
        self.add_requirements(form_data)


class QualificationFormWizard(CookieWizardView):
    template_name = 'qualification_form.html'

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
        context['provider'] = self.qualification.campus.provider
        # make sure logo has been uploaded before set the context
        # otherwise, let it empty
        if self.qualification.campus.provider.provider_logo:
            context['provider_logo'] = \
                self.qualification.campus.provider.provider_logo.url
        return context

    def done(self, form_list, **kwargs):
        form_data = dict()
        for form in form_list:
            if form.prefix == '4':
                context = self.get_context_data(form=form, **kwargs)
                self.add_events(
                    context['view'].storage.data['step_data']['4'])
            else:
                form_data.update(form.cleaned_data)

        qualification_data_process = QualificationFormWizardDataProcess(
            self.qualification
        )
        qualification_data_process.process_data(
            form_data
        )
        url = reverse(
            'show-qualification',
            args=(self.provider.id, self.campus.id, self.qualification.id))
        return redirect(url)

    def add_events(self, step_data):
        new_name = step_data['4-name']
        new_date_start = step_data['4-date_start']
        new_date_end = step_data['4-date_end']
        new_http_link = step_data['4-http_link']
        # Count how many names were submitted and create new_events
        number_of_new_events = len(new_name)
        if len(new_name) == 1 and new_name[0] == '':
            return False
        for i in range(0, number_of_new_events):
            new_qualification_event = QualificationEvent()
            new_qualification_event.name = new_name[i]
            new_date_start_i = new_date_start[i]
            new_date_start_formatted = (
                datetime.strptime(new_date_start_i, '%m/%d/%Y')
            ).strftime('%Y-%m-%d')
            new_date_end_i = new_date_end[i]
            new_date_end_formatted = (
                datetime.strptime(new_date_end_i, '%m/%d/%Y')
            ).strftime('%Y-%m-%d')
            new_qualification_event.date_start = new_date_start_formatted
            new_qualification_event.date_end = new_date_end_formatted
            new_qualification_event.http_link = new_http_link[i]
            try:
                self.new_qualification_events.append(new_qualification_event)
            except AttributeError:
                self.new_qualification_events = []
                self.new_qualification_events.append(new_qualification_event)
        self.qualification.add_events(self.new_qualification_events)

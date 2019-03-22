from django.shortcuts import redirect, Http404, get_object_or_404
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Qualification,
    Requirement,
    Subject,
    QualificationEntranceRequirementSubject,
    QualificationEvent
)
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
    QualificationImportantDatesForm,
)


class QualificationFormWizardDataProcess(object):

    def __init__(self, qualification, post_dict):
        self.qualification = qualification
        self.post_dict = post_dict

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

    def process_data(self, form_data):
        """
        Process qualification form data then update qualification
        :param form_data: dict of form data
        """
        requirement_fields = {}

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
        subject_length = self.post_dict.get('subject-length', 1)
        for subject_index in range(1, int(subject_length) + 1):
            subject = None
            subject_key = '2-subject'
            minimum_score_key = 'subject-minimum-score'
            if subject_index > 1:
                subject_key += f'_{subject_index}'
                minimum_score_key += f'_{subject_index}'
            if subject_key in self.post_dict and self.post_dict[subject_key]:
                subject = Subject.objects.get(
                    id=self.post_dict[subject_key]
                )
            if subject and self.post_dict[minimum_score_key]:
                requirement_subjects, created = (
                    QualificationEntranceRequirementSubject.objects.
                    get_or_create(
                        subject_id=subject,
                        qualification_id=self.qualification,
                    )
                )
                requirement_subjects.minimum_score = (
                    int(self.post_dict[minimum_score_key])
                )
                requirement_subjects.save()

        # Requirement data
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
                qualification_id=self.qualification,
                **requirement_fields
            )

        # Qualification events
        qualification_event_form_fields = (
            vars(QualificationImportantDatesForm)['declared_fields']
        )
        qualification_event_fields = {}
        for qualification_event in qualification_event_form_fields.keys():
            try:
                getattr(QualificationEvent, qualification_event)
                if form_data[qualification_event]:
                    qualification_event_fields[qualification_event] = (
                        form_data[qualification_event]
                    )
            except AttributeError:
                continue
        if qualification_event_fields:
            QualificationEvent.objects.create(
                qualification_id=self.qualification,
                **qualification_event_fields
            )


class QualificationFormWizard(CookieWizardView):
    template_name = 'qualification_form.html'

    @property
    def qualification(self):
        """
        Get qualification from id
        :return: qualification object
        """
        qualification_id = self.request.GET.get('id', None)
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
        return context

    def done(self, form_list, **kwargs):
        form_data = dict()
        for form in form_list:
            form_data.update(form.cleaned_data)
        qualification_data_process = QualificationFormWizardDataProcess(
            self.qualification,
            self.request.POST.dict()
        )
        qualification_data_process.process_data(
            form_data
        )
        return redirect('/')

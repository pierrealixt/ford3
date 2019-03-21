from django.shortcuts import redirect, Http404, get_object_or_404
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Qualification,
    Requirement,
    Subject,
    QualificationEntranceRequirementSubject
)
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm
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
        ]
        return context

    def validate_form_data(self, form_data):
        """
        Validate form data then create new qualification
        :param form_data: dict of form data
        """
        qualification_fields = {}
        requirement_fields = {}

        # Check duration
        if form_data['duration']:
            if form_data['duration_type'] == 'month':
                duration_in_months = form_data['duration']
            else:
                # In years
                duration_in_months = 12 * form_data['duration']
            qualification_fields['duration_in_months'] = duration_in_months

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

        Qualification.objects.filter(
            id=self.qualification.id
        ).update(
            **qualification_fields
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
        post_dict = self.request.POST
        subject_length = post_dict.get('subject-length', 1)
        for subject_index in range(1, int(subject_length) + 1):
            subject = None
            subject_key = '2-subject'
            minimum_score_key = 'subject-minimum-score'
            if subject_index > 1:
                subject_key += f'_{subject_index}'
                minimum_score_key += f'_{subject_index}'
            if subject_key in post_dict and post_dict[subject_key]:
                subject = Subject.objects.get(
                    id=post_dict[subject_key]
                )
            if subject and post_dict[minimum_score_key]:
                requirement_subjects, created = (
                    QualificationEntranceRequirementSubject.objects.
                    get_or_create(
                        subject_id=subject,
                        qualification_id=self.qualification,
                    )
                )
                requirement_subjects.minimum_score = (
                    int(post_dict[minimum_score_key])
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
        Requirement.objects.create(
            qualification_id=self.qualification,
            **requirement_fields
        )

    def done(self, form_list, **kwargs):
        form_data = dict()
        for form in form_list:
            form_data.update(form.cleaned_data)
        self.validate_form_data(form_data)
        return redirect('/')

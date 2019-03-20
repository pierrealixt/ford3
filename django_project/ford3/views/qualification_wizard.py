from django.shortcuts import redirect, Http404, get_object_or_404
from formtools.wizard.views import CookieWizardView
from ford3.models import (
    Qualification,
    Campus
)


class QualificationFormWizard(CookieWizardView):
    template_name = 'qualification_form.html'
    campus = Campus.objects.none()
    qualification_field_list = [
        'short_description',
        'long_description',
        'nqf_level'
    ]

    def qualification_campus(self, campus_id):
        """
        Get campus from campus id
        :param campus_id: id of campus
        :return: campus object
        """
        if not campus_id:
            raise Http404()
        return get_object_or_404(
            Campus,
            id=campus_id
        )

    def get(self, *args, **kwargs):
        campus_id = self.request.GET.get('campus_id', None)
        self.qualification_campus(campus_id)
        return super(QualificationFormWizard, self).get(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['form_name_list'] = [
            'Details',
            'Duration & Fees',
            'Requirements'
        ]
        return context

    def validate_form_data(self, form_data):
        """
        Validate form data then create new qualification
        :param form_data: dict of form data
        """
        qualification_fields = {}

        # Check duration
        if form_data['duration']:
            if form_data['duration_type'] == 'month':
                duration_in_months = form_data['duration']
            else:
                # In years
                duration_in_months = 12 * form_data['duration']
            qualification_fields['duration_in_months'] = duration_in_months

        for qualification_field in self.qualification_field_list:
            qualification_fields[qualification_field] = (
                form_data[qualification_field]
            )

        qualification = Qualification.objects.create(
            campus_id=self.campus,
            **qualification_fields
        )

    def done(self, form_list, **kwargs):
        campus_id = self.request.GET.get('campus_id', None)
        self.campus = self.qualification_campus(campus_id)
        form_data = dict()
        for form in form_list:
            form_data.update(form.cleaned_data)
        self.validate_form_data(form_data)
        return redirect('/')

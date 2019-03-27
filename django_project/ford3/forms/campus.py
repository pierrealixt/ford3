# coding=utf-8
from django import forms
from crispy_forms.helper import FormHelper


class CampusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CampusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_error_title = 'Form Errors'
        self.helper.help_text_inline = True


class CampusDetailForm(CampusForm):

    photo = forms.FileField(
        required=False)

    telephone = forms.CharField(
        label='Tel. Number:',
        required=False)

    email = forms.CharField(
        label='Email:',
        required=False)

    max_students_per_year = forms.IntegerField(
        label='Maximum number of Students per year in campus',
        required=False)


class CampusLocationForm(CampusForm):
    physical_address = forms.CharField(
        label='Address',
        required=False)


class CampusImportantDatesForm(CampusForm):
    date_start = forms.DateField(
        label='Application period start:',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'col-md-4'}
        )
    )

    date_end = forms.DateField(
        label='Application period end:',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'col-md-4'}
        )
    )

    other_event = forms.CharField(
        label='Other event [if any]:',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Title, eg, Exhibition'}
        )
    )

    event_date = forms.DateField(
        label='Event Date:',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'col-md-4'}
        )
    )


class CampusQualificationsForm(CampusForm):
    qualification_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

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

    # photo = forms.FileField(
    #     required=False)

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
    physical_address_street_name = forms.CharField(
        label='Street name',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Street name'}
        ))

    physical_address_city = forms.CharField(
        required=False,
        label='City',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'
            }
        ))

    physical_address_postal_code = forms.CharField(
        required=False,
        label='Postal code',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Postal code'
            }
        ))

    is_physical_addr_same_as_postal_addr = forms.TypedChoiceField(
        label='Is Postal Address different to Physical Address',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect
    )


class CampusImportantDatesForm(CampusForm):
    event_name = forms.CharField(
        label='Event name',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Open day, ...'}
        )
    )

    date_start = forms.DateField(
        label='Starting date:',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'col-md-4'}
        )
    )

    date_end = forms.DateField(
        label='Ending date',
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'col-md-4'}
        )
    )

    http_link = forms.CharField(
        label='Link to event',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'http://...'}
        )
    )


class CampusQualificationsForm(CampusForm):
    saqa_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

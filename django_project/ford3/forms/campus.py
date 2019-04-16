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
    physical_address_line_1 = forms.CharField(
        label='Physical Address',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Line 1'}
        ))
    physical_address_line_2 = forms.CharField(
        label=' ',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Line 2'}
        ))

    physical_address_city = forms.CharField(
        required=False,
        label=' ',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'
            }
        ))

    physical_address_postal_code = forms.CharField(
        required=False,
        label=' ',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Postal code'
            }
        ))

    postal_address_differs = forms.BooleanField(
        label='Postal address is different.',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(),
    )

    postal_address_line_1 = forms.CharField(
        label='Postal Address',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Line 1'}
        ))
    postal_address_line_2 = forms.CharField(
        label=' ',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Line 2'}
        ))

    postal_address_city = forms.CharField(
        required=False,
        label=' ',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'
            }
        ))

    postal_address_postal_code = forms.CharField(
        required=False,
        label=' ',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Postal code'
            }
        ))


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

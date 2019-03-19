from django import forms
from crispy_forms.helper import FormHelper


class QualificationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QualificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_error_title = 'Form Errors'
        self.helper.help_text_inline = True


class QualificationDetailForm(QualificationForm):
    short_description = forms.CharField(
        label='Short Description of this Qualification:',
        help_text='*120 character max',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': '5'}
        ),
        max_length=120
    )
    long_description = forms.CharField(
        label='Long Description of this Qualification:',
        help_text='*500 character max',
        required=False,
        widget=forms.Textarea,
        max_length=500
    )
    nqf_level = forms.IntegerField(
        label='NQF Level on completion:',
        help_text='*Populated from SAQA'
    )
    distance_learning = forms.BooleanField(
        label='Distance Learning',
        required=False
    )


class QualificationDurationFeesForm(QualificationForm):
    full_time_qualification = forms.BooleanField(
        label='Full-Time Qualification',
        required=False
    )

    part_time_qualification = forms.BooleanField(
        label="Part-Time Qualification",
        required=False
    )

    duration = forms.IntegerField(
        label='Duration of the Qualification',
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'col-md-4'}
        )
    )

    duration_type = forms.ChoiceField(
        label=' ',
        choices=[
            ('month', 'Month'),
            ('year', 'Year')
        ],
        required=False,
        widget=forms.Select(
            attrs={'class': 'col-md-4'}
        )
    )

    total_cost = forms.DecimalField(
        label='Total Cost of Qualification',
        widget=forms.TextInput(
            attrs={'placeholder': 'ZAR'}
        )
    )

    total_cost_comment = forms.CharField(
        label='Cost Comment Field',
        help_text='*Any extra comments on '
                  'how Costs of this Qualification work',
        required=False,
        max_length=255
    )

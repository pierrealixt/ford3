from django import forms
from crispy_forms.helper import FormHelper
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel
from ford3.models.interest import Interest


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
        label='Short description of this qualification',
        help_text='*120 characters max '
                  '- This field is required for publication',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': '2',
                'placeholder': 'Brief summary of the qualification'}
        ),
        max_length=120
    )
    long_description = forms.CharField(
        label='Long description of this qualification',
        help_text='*500 characters max',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': '5',
                'cols': '40',
                'placeholder': 'Write full description of the qualification'}
        ),
        max_length=500
    )
    distance_learning = forms.TypedChoiceField(
        label='Distance learning',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect
    )


class QualificationDurationFeesForm(QualificationForm):
    full_time = forms.TypedChoiceField(
        label='Type of the qualification',
        help_text='<br>This field is required for publication',
        coerce=lambda x: x == 'True',
        choices=((True, 'Full-time'), (False, 'Part-time')),
        required=False,
        widget=forms.RadioSelect
    )

    duration = forms.IntegerField(
        label='Duration of the qualification',
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'col-md-4', 'placeholder': '6 months or 2 years'}
        )
    )

    duration_time_repr = forms.ChoiceField(
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
        label='Total cost of the qualification',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'ZAR'}
        )
    )

    total_cost_comment = forms.CharField(
        label='Cost comment field',
        help_text='*Any extra comments on '
                  'how Costs of this Qualification work',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Additional info regarding costs',
                'cols': '40',
                'rows': '10'}
        ),
        max_length=255
    )


class QualificationRequirementsForm(QualificationForm):
    min_nqf_level = forms.ChoiceField(
        label='Required entrance qualification',
        help_text='*List from SAQA '
                  '- This field is required for publication',
        required=False,
        choices=[('', '-')] + [
            (level, level.value) for level in SaqaQualificationLevel]
    )

    interview = forms.TypedChoiceField(
        label='Is there an interview?',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect
    )

    portfolio = forms.TypedChoiceField(
        label='Does it require a portfolio?',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect(
            attrs={
                'data-disabler': 'portfolio'
            }
        )
    )

    portfolio_comment = forms.CharField(
        label='What does the portfolio require?',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': '5',
                'placeholder': 'What does the portfolio require?',
                'data-field': 'portfolio'
            }
        ),
        max_length=120
    )

    require_aps_score = forms.TypedChoiceField(
        label='Does it require an APS score?',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect(
            attrs={
                'data-disabler': 'aps-score'
            }
        )
    )

    aps_calculator_link = forms.URLField(
        label='Link to APS Calculator',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'www.example/aps.com',
                'data-field': 'aps-score'
            }
        )
    )

    require_certain_subjects = forms.TypedChoiceField(
        label='Does the qualification require certain subjects?',
        help_text='<br>If "Yes", please add at least one required subject if '
                  'you wish to publish this qualification',
        coerce=lambda x: x == 'True',
        required=False,
        choices=((True, 'Yes'), (False, 'No')),
        widget=forms.RadioSelect()
    )

    # (subject_id, min_score), (..., ...), ...
    subjects_scores = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )


class QualificationInterestsAndJobsForm(QualificationForm):
    interest_list = forms.ModelMultipleChoiceField(
        label='Choose three interests associated to this qualification',
        queryset=Interest.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'data-background-color': 'turquoise',
                'data-max-selected': '3'
            }
        )
    )

    occupations_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

    critical_skill = forms.BooleanField(
        label=(
            'This qualification prepares a learner for a '
            '<b>critical skills</b> occupation.'
        ),
        required=False,
    )

    green_occupation = forms.BooleanField(
        label=(
            'This qualification prepares a learner for a <b>green</b> '
            'occupation.'
        ),
        required=False,
    )

    high_demand_occupation = forms.BooleanField(
        label=(
            'This qualification prepares a learner for a <b>high demand</b> '
            'occupation.'
        ),
        required=False,
    )


class QualificationImportantDatesForm(QualificationForm):
    event_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)

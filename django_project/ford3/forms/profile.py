from django import forms
from crispy_forms.helper import FormHelper


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_error_title = 'Form Errors'
        self.helper.help_text_inline = True

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'John'}
        ),
        required=True,
        max_length=100
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'Doe'}
        ),
        required=True,
        max_length=100
    )
    email = forms.EmailField(
        label='E-mail address',
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        required=True
    )

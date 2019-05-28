from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class UserAccountActivationForm(forms.Form):
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
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New Password'}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Re-type new password'}
        ),
    )
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        super(UserAccountActivationForm, self).__init__(
            *args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

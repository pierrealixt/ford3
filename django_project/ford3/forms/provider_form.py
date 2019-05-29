from django import forms
from django.core.exceptions import ValidationError
from ford3.models.provider import Provider
from ford3.models.province import Province



EMPTY_TEL_ERROR = 'Your telephone number is required.'
EMPTY_EMAIL_ERROR = 'Your email is required.'


class ProviderForm(forms.models.ModelForm):

    class Meta:
        model = Provider
        fields = (
            'name',
            'province',
            'provider_type',
            'telephone',
            'admissions_contact_no',
            'email',
            'website',
            'physical_address_line_1',
            'physical_address_line_2',
            'physical_address_city',
            'physical_address_postal_code',
            'postal_address_differs',
            'postal_address_line_1',
            'postal_address_line_2',
            'postal_address_city',
            'postal_address_postal_code',
            'provider_logo',)
        widgets = {
            'name' : forms.fields.TextInput(
                attrs={'placeholder': "Provider's name"}
            ),
            'province': forms.fields.Select(
                choices=Province.to_form(),
                attrs={'class' : 'edu-button edu-dropdown-button'}),
            'provider_type' : forms.fields.Select(
                choices=Provider.types_to_form(),
                attrs={'class' : 'edu-button edu-dropdown-button'}),
            'telephone': forms.fields.TextInput(
                attrs={'placeholder': 'Primary contact number'}),
            'admissions_contact_no' : forms.fields.TextInput(
                attrs={'placeholder': 'Admissions contact number'}),
            'email': forms.fields.EmailInput(
                attrs={'placeholder': 'example@example.com'}),
            'website': forms.fields.URLInput(
                attrs={'placeholder': 'www.yourwebsitename.com'}),
            'physical_address_line_1': forms.fields.TextInput(
                attrs={'placeholder': 'Address Line 1'}),
            'physical_address_line_2': forms.fields.TextInput(
                attrs={'placeholder': 'Address Line 2'}),
            'physical_address_city': forms.fields.TextInput(
                attrs={'placeholder': 'City'}),
            'physical_address_postal_code': forms.fields.TextInput(
                attrs={'placeholder': 'Postal/ZIP Code'}),
            'postal_address_differs' : forms.fields.CheckboxInput(),
            'postal_address_line_1': forms.fields.TextInput(
                attrs={'placeholder': 'Address Line 1'}),
            'postal_address_line_2': forms.fields.TextInput(
                attrs={'placeholder': 'Address Line 2'}),
            'postal_address_city': forms.fields.TextInput(
                attrs={'placeholder': 'City'}),
            'postal_address_postal_code': forms.fields.TextInput(
                attrs={'placeholder': 'Postal/ZIP Code'}),
        }
        error_messages = {
            'telephone': {'required': EMPTY_TEL_ERROR},
            'email' : {'required': EMPTY_EMAIL_ERROR}
        }

    def clean_provider_logo(self):
        provider_logo = self.cleaned_data.get('provider_logo', False)
        if provider_logo:
            if provider_logo.size > 100 * 1024:
                raise ValidationError("Max file size is 100Kb")
            return provider_logo

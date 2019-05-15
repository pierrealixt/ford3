from django import forms
from ford3.models.prospect import Prospect


class ProspectForm(forms.models.ModelForm):
    class Meta:
        model = Prospect
        name = forms.CharField(label='Your name', required=True)
        fields = ['name', 'telephone', 'email']

        widgets = {
            'name': forms.fields.TextInput(
                attrs={'placeholder': 'John Doe'}),
            'telephone': forms.fields.TextInput(
                attrs={'placeholder': '021 345 678'}),
            'email': forms.fields.EmailInput(
                attrs={'placeholder': 'johndoe@email.com'}),
        }

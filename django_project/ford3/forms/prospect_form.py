from django import forms
from ford3.models.prospect import Prospect


class ProspectForm(forms.models.ModelForm):
    class Meta:
        model = Prospect
        name = forms.CharField(label='Your name', required=True)
        fields = ['name', 'telephone', 'email']

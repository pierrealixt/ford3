from django import forms
from ford3.models.prospect import Prospect

class ProspectForm(forms.models.ModelForm):
    class Meta:
        model = Prospect
        fields = ['name', 'telephone', 'email']

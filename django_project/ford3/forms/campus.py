# coding=utf-8
from django import forms

from ford3.models import Campus


class CampusDetailsForm(forms.ModelForm):

    class Meta:
        model = Campus
        fields = ['photo', 'telephone', 'email', 'max_students_per_year']

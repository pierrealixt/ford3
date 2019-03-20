# coding=utf-8
from django.conf.urls import url
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm
)
from ford3.views.qualification_wizard import QualificationFormWizard

qualification_wizard = QualificationFormWizard.as_view(
    [
        QualificationDetailForm,
        QualificationDurationFeesForm,
        QualificationRequirementsForm
    ],
)

urlpatterns = [
    url(
        r'^qualification-form/$',
        qualification_wizard,
        name='qualification_form'
    ),
]

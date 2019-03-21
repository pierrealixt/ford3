# coding=utf-8
from django.conf.urls import url
from django.urls import path
from ford3.forms import CampusDetailsForm
from ford3.views.views import CampusWizard
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
    QualificationImportantDatesForm,
)
from ford3.views.qualification_wizard import QualificationFormWizard

qualification_wizard = QualificationFormWizard.as_view(
    [
        QualificationDetailForm,
        QualificationDurationFeesForm,
        QualificationRequirementsForm,
        QualificationInterestsAndJobsForm,
        QualificationImportantDatesForm,
    ],
)

urlpatterns = [
    url(
        r'^qualification-form/$',
        qualification_wizard,
        name='qualification_form'
    ),
    path('campus/', CampusWizard.as_view([
        ('Details', CampusDetailsForm),
    ])),
]

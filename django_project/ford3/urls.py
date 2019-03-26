# coding=utf-8
from django.urls import path
from ford3.views import views
from django.conf.urls import url
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm,
    QualificationRequirementsForm,
    QualificationInterestsAndJobsForm,
    QualificationImportantDatesForm,
)
from ford3.views.qualification_wizard import QualificationFormWizard
from ford3.forms.campus import (
    CampusDetailForm,
    CampusLocationForm,
    CampusImportantDatesForm,
    # CampusQualificationsForm
)
from ford3.views.campus_wizard import CampusFormWizard

qualification_wizard = QualificationFormWizard.as_view(
    [
        QualificationDetailForm,
        QualificationDurationFeesForm,
        QualificationRequirementsForm,
        QualificationInterestsAndJobsForm,
        QualificationImportantDatesForm,
    ],
)

campus_wizard = CampusFormWizard.as_view(
    [
        CampusDetailForm,
        CampusLocationForm,
        CampusImportantDatesForm,
        # CampusQualificationsForm
    ]
)

urlpatterns = [
    url(
        r'^qualification-form/$',
        qualification_wizard,
        name='qualification_form'
    ),
    url(r'^ProviderForm/$', views.provider_form, name='provider_form'),
    url(r'^TestWidgets/$', views.widget_examples, name='test_widgets'),
    path('campus/<int:campus_id>/edit', campus_wizard, name='campus_form')
]

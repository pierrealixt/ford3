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
    CampusQualificationsForm
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
        CampusQualificationsForm
    ]
)

urlpatterns = [
    url(
        r'^qualification-form/$',
        qualification_wizard,
        name='qualification_form'
    ),
    path('providers/<int:provider_id>/',
         views.show_provider,
         name='show_provider'),
    path('providers/<int:provider_id>/edit',
         views.edit_provider,
         name='provider_form'),
    path(
        'providers/<int:provider_id>/campus/<int:campus_id>/edit',
        campus_wizard,
        name='campus_form'),
    path(
        'providers/<int:provider_id>/campus/<int:campus_id>',
        views.show_campus,
        name='campus'),
    path(
        'saqa_qualifications',
        views.saqa_qualifications,
        name='saqa_qualifications'),

    url(r'^test_widgets/$', views.widget_examples, name='test_widgets'),
]

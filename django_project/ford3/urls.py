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
from ford3.views.provider import show_provider, edit_provider

qualification_wizard = QualificationFormWizard.as_view(
    [
        QualificationDetailForm,
        QualificationDurationFeesForm,
        QualificationRequirementsForm,
        QualificationInterestsAndJobsForm,
        QualificationImportantDatesForm,
    ],
)

CAMPUS_FORMS = [
    ('campus-details', CampusDetailForm),
    ('campus-location', CampusLocationForm),
    ('campus-dates', CampusImportantDatesForm),
    ('campus-qualifications', CampusQualificationsForm)
]

campus_wizard = CampusFormWizard.as_view(CAMPUS_FORMS)

urlpatterns = [
    path('providers/<int:provider_id>',
         show_provider,
         name='show-provider'),
    path('providers/<int:provider_id>/edit',
         edit_provider,
         name='edit-provider'),
    path(
        'providers/<int:provider_id>/campus/<int:campus_id>/edit',
        campus_wizard,
        name='edit-campus'),
    path(
        'providers/<int:provider_id>/campus/<int:campus_id>',
        views.show_campus,
        name='show-campus'),
    path(
        'saqa_qualifications',
        views.saqa_qualifications,
        name='search-saqa-qualifications'),
    path(
        '/'.join([
            'providers/<int:provider_id>',
            'campus/<int:campus_id>',
            'qualifications/<int:qualification_id>/edit']),
        qualification_wizard,
        name='edit-qualification'),
    path(
        '/'.join([
            'providers/<int:provider_id>',
            'campus/<int:campus_id>',
            'qualifications/<int:qualification_id>']),
        views.show_qualification,
        name='show-qualification'),
    url(r'^test_widgets/$', views.widget_examples, name='test_widgets'),
]

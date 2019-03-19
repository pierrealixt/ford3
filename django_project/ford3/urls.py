# coding=utf-8
from django.conf.urls import url
from ford3.forms.qualification import (
    QualificationDetailForm,
    QualificationDurationFeesForm
)
from ford3.views.qualification_wizard import QualificationFormWizard

qualification_wizard = QualificationFormWizard.as_view(
    [QualificationDetailForm, QualificationDurationFeesForm],
    url_name='qualification_step',
    done_step_name='finished'
)

urlpatterns = [
    url(r'^qualification-form/(?P<step>.+)/$',
        qualification_wizard,
        name='qualification_step'),
    url(
        r'^qualification-form/$',
        qualification_wizard,
        name='qualification_form'
    ),
]

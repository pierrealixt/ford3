# coding=utf-8
from django.urls import path

from ford3.forms import CampusDetailsForm
from ford3.views.views import CampusWizard

urlpatterns = [
    path('campus/', CampusWizard.as_view([
        ('Details', CampusDetailsForm),
    ])),
]

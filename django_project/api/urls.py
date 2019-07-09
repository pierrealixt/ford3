from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from api.viewsets.provider import ProvidersViewSet
from api.viewsets.qualification import QualificationViewSet
from api.viewsets.campus import CampusViewSet
from api.viewsets.campus_event import CampusEventViewSet
from api.viewsets.qualification_event import QualificationEventViewSet
from api.viewsets.saqa_qualification import SAQAQualificationViewSet


urlpatterns = [
    url(r'^(?P<version>(v1))/providers/$',
        ProvidersViewSet.as_view({'get': 'list'}),
        name='show-providers-api'),

    url(r'^(?P<version>(v1))/providers/(?P<pk>\d+)/$',
        ProvidersViewSet.as_view({'get': 'retrieve'}),
        name='show-provider-api'),

    url(r'^(?P<version>(v1))/campus/$',
        CampusViewSet.as_view({'get': 'list'}),
        name='show-campuses-api'),

    url(r'^(?P<version>(v1))/campus/(?P<pk>\d+)/$',
        CampusViewSet.as_view({'get': 'retrieve'}),
        name='show-campus-api'),

    url(r'^(?P<version>(v1))/qualifications/$',
        QualificationViewSet.as_view({'get': 'list'}),
        name='show-qualifications-api'),

    url(r'^(?P<version>(v1))/qualifications/(?P<pk>\d+)/$',
        QualificationViewSet.as_view({'get': 'retrieve'}),
        name='show-qualification-api'),

    url(r'^(?P<version>(v1))/qualification-events/$',
        QualificationEventViewSet.as_view({'get': 'list'}),
        name='show-qualification-events-api'),

    url(r'^(?P<version>(v1))/qualification-events/(?P<pk>\d+)/$',
        QualificationEventViewSet.as_view({'get': 'retrieve'}),
        name='show-qualification-event-api'),

    url(r'^(?P<version>(v1))/saqa-qualifications/$',
        SAQAQualificationViewSet.as_view({'get': 'list'}),
        name='show-saqa-qualifications-api'),

    url(r'^(?P<version>(v1))/saqa-qualifications/(?P<pk>\d+)/$',
        SAQAQualificationViewSet.as_view({'get': 'retrieve'}),
        name='show-saqa-qualification-api'),

    url(r'^(?P<version>(v1))/campus-events/$',
        CampusEventViewSet.as_view({'get': 'list'}),
        name='show-campus-events-api'),

    url(r'^(?P<version>(v1))/campus-events/(?P<pk>\d+)/$',
        CampusEventViewSet.as_view({'get': 'retrieve'}),
        name='show-campus_event-api'),
    url(r'^docs/', include_docs_urls(title='OpenEdu API v1'))
]

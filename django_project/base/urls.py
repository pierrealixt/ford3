# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import patterns, url
from django.conf import settings

from views import Home, custom_404 

urlpatterns = patterns(
    '',
    # basic app views
    url(regex='^$',
        view=Home.as_view(),
        name='home'),
)

# Prevent cloudflare from showing an ad laden 404 with no context
handler404 = custom_404

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))

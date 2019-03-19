# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import url, include

from .views import Home, custom_404

urlpatterns = [
    # basic app views
    url(regex='^$',
        view=Home.as_view(),
        name='home'),
    url(r'^', include('ford3.urls')),
]

# Prevent cloudflare from showing an ad laden 404 with no context
handler404 = custom_404

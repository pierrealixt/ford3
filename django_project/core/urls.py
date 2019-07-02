# coding=utf-8
"""Project level url handler."""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from sentry_sdk import capture_message
from ford3.forms.custom_auth_form import CustomAuthForm


# from django.conf.urls.static import static

admin.autodiscover()
handler404 = 'base.views.error_views.custom_404'


def handler500(request, template_name='500.html', *args, **kwargs):
    """500 error handler which includes ``request`` in the context.

    See http://raven.readthedocs.org/en/latest/integrations/
        django.html#message-references

    :param request: Django request object.

    Templates: `500.html`
    Context: None
    """
    capture_message("Page not found!", level="error")

    # You need to create a 500.html template.
    response = render(
        request,
        template_name,
        context={
            'request': request
        },
        status=500)
    return response


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^site-admin/', admin.site.urls),
    url(r'^', include('ford3.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('base.urls')),
    url(
        r'^accounts/login/$',
        auth_views.LoginView.as_view(authentication_form=CustomAuthForm),
        name='login'),
    url(
        r'^logout/$',
        auth_views.LogoutView.as_view(), {'next_page': '/'},
        name='logout'),
    url(r'^api-auth/', include('rest_framework.urls')),

    # API Examples
    url(r'api-examples/$', TemplateView.as_view(
        template_name='api-examples/index.html')),

    url(r'api-examples/providers/$', TemplateView.as_view(
        template_name='api-examples/providers.html')),
    url(r'api-examples/calendar/$', TemplateView.as_view(
        template_name='api-examples/calendar.html')),
    url(r'api-examples/map/$', TemplateView.as_view(
        template_name='api-examples/map.html')),

]

if settings.DEBUG:
    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

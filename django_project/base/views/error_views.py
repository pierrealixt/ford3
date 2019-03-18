# coding=utf-8
"""Our custom error views."""
from django.shortcuts import render


def custom_404(request, template_name='404.html', *args, **kwargs):
    """Our custom 404 view

    :param template_name: The template to render
    :type template_name: str

    :return: Response obj
    :rtype: HttpResponse

    """
    response = render(
        request,
        template_name,
        context={
            'request_path': request.path
        },
        status=404)
    return response

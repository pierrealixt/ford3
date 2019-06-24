from django.shortcuts import redirect
from django.urls import reverse
from ford3.models.user import User
from ford3.models.campus import Campus
from ford3.models.qualification import Qualification


def predicate_provider(user, provider_id):
    user = User.set_user_from_type(user)
    return provider_id in [p['id'] for p in user.providers]


def provider_check(view_func):
    def wrapper(request, **kwargs):
        if predicate_provider(request.user, kwargs['provider_id']):
            return view_func(request, **kwargs)
        else:
            return redirect(reverse('dashboard'))
    return wrapper



def predicate_campus(provider_id, campus_id):
    return Campus.objects.filter(
        pk=campus_id,
        provider_id=provider_id).exists()


def campus_check(view_func):
    def wrapper(request, **kwargs):
        if predicate_campus(kwargs['provider_id'], kwargs['campus_id']):
            return view_func(request, **kwargs)
        else:
            return redirect(reverse('dashboard'))
    return wrapper


def predicate_qualification(campus_id, qualification_id):
    return Qualification.objects.filter(
        pk=qualification_id,
        campus_id=campus_id).exists()


def qualification_check(view_func):
    def wrapper(request, **kwargs):
        if predicate_qualification(
            kwargs['campus_id'],
            kwargs['qualification_id']):
            return view_func(request, **kwargs)
        else:
            return redirect(reverse('dashboard'))
    return wrapper

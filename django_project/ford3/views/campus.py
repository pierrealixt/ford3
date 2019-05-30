from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from ford3.models.campus import Campus
from ford3.models.provider import Provider


@login_required
def show(request, provider_id, campus_id):
    campus = get_object_or_404(
        Campus,
        id=campus_id)
    form_data = {
        'provider_name': campus.provider.name
    }
    context = {
        'form_data': form_data,
        'campus': campus,
        'provider': campus.provider,
        # make sure logo has been uploaded before set the context
        # otherwise, let it empty
        'provider_logo':
            campus.provider.provider_logo.url
            if campus.provider.provider_logo else ""
    }

    return render(request, 'campus.html', context)


@login_required()
def create(request, provider_id):
    if request.method == 'GET':
        url = reverse('show-provider', args=[str(provider_id)])
        return redirect(url)

    provider = get_object_or_404(
        Provider,
        id=provider_id)

    context = {
        'provider': provider
    }

    try:
        provider.campus_set.create(
            name=request.POST['campus_name'],
            created_by=request.user,
            edited_by=request.user)
        context['campus_success'] = 'Campus successfully created.'
    except ValidationError as ve:
        context['campus_error'] = '<br />'.join(ve.messages)
    except MultiValueDictKeyError:
        # arg campus_name not present in request.POST
        context['campus_error'] = 'Bad request.'

    return render(request, 'provider.html', context)

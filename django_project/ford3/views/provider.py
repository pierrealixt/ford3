from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404)
from django.db import IntegrityError
from django.urls import reverse
from ford3.forms.provider_form import ProviderForm
from ford3.models.provider import Provider


@login_required()
@permission_required('ford3.add_provider', raise_exception=True)
@require_http_methods(['GET'])
def new(request):
    context = {
        'form': ProviderForm(),
        'is_new_provider': True,
        'submit_url': reverse('create-provider')
    }
    return render(
        request,
        'provider_form.html',
        context)


@login_required()
@permission_required('ford3.add_provider', raise_exception=True)
@require_http_methods(['POST'])
def create(request):
    form = ProviderForm(request.POST, request.FILES)
    if form.is_valid():
        provider = form.save(commit=False)
        try:
            provider.created_by = request.user
            provider.edited_by = request.user
            provider.save()

            provider.create_campus(
                request.POST.getlist('campus_name'),
                request.user)
        except IntegrityError:
            return render(request, 'provider_form.html', {'form': form})

        redirect_url = reverse(
            'show-provider',
            args=[str(provider.id)])
        return redirect(redirect_url)
    else:
        context = {
            'form': form,
            'is_new_provider': True,
            'submit_url': reverse('create-provider')
        }
        return render(request, 'provider_form.html', context)



@login_required()
@permission_required('ford3.change_provider', raise_exception=True)
@require_http_methods(['GET'])
def edit(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id)
    form = ProviderForm(instance=provider)
    submit_url = reverse(
        'update-provider',
        args=[str(provider.id)])
    context = {
        'form': form,
        'submit_url': submit_url
    }
    return render(
        request,
        'provider_form.html',
        context)


@login_required()
@permission_required('ford3.change_provider', raise_exception=True)
@require_http_methods(['POST'])
def update(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id)
    form = ProviderForm(request.POST, request.FILES, instance=provider)
    if form.is_valid():
        provider = form.save()
        provider.edited_by = request.user
        provider.save()
        redirect_url = reverse(
            'show-provider',
            args=[str(provider.id)])
    else:
        submit_url = reverse(
            'update-provider',
            args=[str(provider.id)])
        context = {
            'form': form,
            'submit_url': submit_url
        }

        return render(
            request,
            'provider_form.html',
            context)

    return redirect(redirect_url)


@login_required
@require_http_methods(['GET'])
def show(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    context = {
        'provider': provider
    }
    # make sure logo has been uploaded before set the context
    # otherwise, let it empty
    if provider.provider_logo:
        context['provider_logo'] = provider.provider_logo.url

    return render(request, 'provider.html', context)


@login_required()
@permission_required('ford3.delete_provider', raise_exception=True)
@require_http_methods(['GET'])
def delete(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    provider.deleted = True
    provider.deleted_by = request.user
    provider.save()

    return redirect(reverse('dashboard'))

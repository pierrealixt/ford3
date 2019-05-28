from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from ford3.models.province import Province
from ford3.models.provider import Provider


@login_required
def show(request):
    user = request.user
    user_id = user.id
    if user.is_province:  # Province user sees all providers in his province
        user_provinces: user.provinces_set.all()
        i = 0
        # providers = Provider.objects.filter(province_id=user_province.id)
    elif user.is_provider:  # Provider user
        providers = Provider.objects.filter(users__id=user_id)
    elif user.is_campus:  # Campus user
        provider_user = user.creator
        providers = Provider.objects.filter(users__id=provider_user.id)
    else:
        return redirect(reverse('home'))
    context = {
        'providers': providers
    }
    return render(request, 'dashboard.html', context)

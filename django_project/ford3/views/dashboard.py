from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from ford3.models.province import Province
from ford3.models.provider import Provider
from ford3.models.user import User


@login_required
def show(request):
    user = User.set_user_from_type(request.user)
    context = {
        'providers': user.providers,
        'is_dashboard': True
    }

    return render(request, 'dashboard.html', context)

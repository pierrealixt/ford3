from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ford3.models.user import User


@login_required
def show(request):
    user = User.set_user_from_type(request.user)

    context = {
        'providers': list(user.providers)
    }

    return render(request, 'dashboard.html', context)

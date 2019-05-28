from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def show(request):
    context = {}
    return render(request, 'dashboard.html', context)

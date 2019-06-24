from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from ford3.forms.profile import ProfileForm
from ford3.forms.user_account_activation import UserAccountActivationForm
from ford3.models.user import User
from ford3.tokens import account_activation_token


@login_required
@require_http_methods(['GET'])
def show(request):
    user = request.user
    data = {'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}
    context = {
        'form': ProfileForm(data),
        'title': 'Profile'
    }
    return render(request, 'account/profile.html', context)


@login_required
@require_http_methods(['POST'])
def edit(request):
    user = request.user
    # form = ProfileForm(request.POST)
    form = ProfileForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        data['message'] = 'Details successfully updated.'
    context = {
        'form': form,
        'data': data,
    }
    return render(request, 'account/profile.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = UserAccountActivationForm(
                data=request.POST,
                user=user)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                password = form.cleaned_data["new_password1"]
                user.set_password(password)
                user.is_active = True
                user.save()
                login(
                    request,
                    user,
                    backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse('dashboard'))
            else:
                return render(
                    request,
                    'account/activation_form.html',
                    {'form': form})
        else:
            if user.is_active:
                return redirect(reverse('dashboard'))
            else:
                return render(
                    request,
                    'account/activation_form.html',
                    {'form': UserAccountActivationForm()})

    else:
        return render(request, 'account/activation_invalid.html')

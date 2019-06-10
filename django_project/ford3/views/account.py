import datetime
from pytz import UTC
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login
from django.urls import reverse
from ford3.models.user import User
from ford3.forms.user_account_activation import UserAccountActivationForm
from ford3.tokens import account_activation_token


class ActivationInvalid(Exception):
    pass


def check_user_activation(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise ActivationInvalid

    if account_activation_token.check_token(user, token):
        return user
    else:
        # the token does not exist anymore
        # By including the user's hashed password and last login timestamp
        # in the hash, a token is automatically invalidated
        # when the user logs in or changes their password
        raise ActivationInvalid



def activate(request, uidb64, token):
    try:
        user = check_user_activation(uidb64, token)
    except ActivationInvalid:
        return render(request, 'account/activation_invalid.html')

    if request.method == "POST":
        form = UserAccountActivationForm(
            data=request.POST,
            user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.account_activated = True
            password = form.cleaned_data["new_password1"]
            user.set_password(password)
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

    return render(
        request,
        'account/activation_form.html',
        {'form': UserAccountActivationForm()})

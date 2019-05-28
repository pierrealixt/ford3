from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from ford3.models.user import User


class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['ford3.view_user']
    model = User

    def get_queryset(self):
        if self.request.user.is_province:
            return User.objects.filter(is_provider=True)
        elif self.request.user.is_provider:
            return User.objects.filter(is_campus=True)


class UserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ['ford3.add_user']
    model = User
    fields = ['email']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.object.email

        if self.request.user.is_province:
            # province user creates provider user
            self.object.is_provider = True
        elif self.request.user.is_provider:
            # provider user creates campus user
            self.object.is_campus = True
        self.object.save()
        return HttpResponseRedirect(reverse('dashboard-users'))

from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from ford3.models.user import User


class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['ford3.view_user']
    model = User

    def get_queryset(self):
        return User \
            .set_user_from_type(self.request.user) \
            .users


class UserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ['ford3.add_user']
    model = User
    fields = ['email']

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.request.user.is_province:
            # province user creates provider user
            self.object.is_provider = True
        elif self.request.user.is_provider:
            # provider user creates campus user
            self.object.is_campus = True
        self.object.creator = self.request.user
        try:
            self.object.save()
        except IntegrityError:
            return self.render_to_response(self.get_context_data(
                form=form,
                form_error='Email already present in the database.'))

        return HttpResponseRedirect(reverse('dashboard-users'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

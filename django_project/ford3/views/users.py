from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required, permission_required


from ford3.models.user import User


# https://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# @login_required()
# @permission_required('ford3.view_user', raise_exception=True) # noqa
class UserList(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        if self.request.user.is_province:
            return User.objects.filter(is_provider=True)


# @login_required()
# @permission_required('ford3.add_user', raise_exception=True) # noqa
class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    fields = ['email', 'username']

    def form_valid(self, form):
        # https://stackoverflow.com/questions/32998300/django-createview-how-to-perform-action-upon-save
        self.object = form.save()
        self.object.username = self.object.email
        if self.request.user.is_province:
            # province user creates provider user
            self.object.is_provider = self.request.user.is_province
        elif self.request.user.is_provider:
            # self.object.creator = self.request.user
            # provider user creates campus user
            self.object.is_campus = self.request.user.is_provider
        self.object.save()
        return HttpResponseRedirect(reverse('dashboard-users'))

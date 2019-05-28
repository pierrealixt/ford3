from itertools import chain
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from ford3.enums.open_edu_groups import OpenEduGroups


class User(AbstractUser):
    is_province = models.BooleanField(
        'province status', default=False)
    is_provider = models.BooleanField(
        'provider status', default=False)
    is_campus = models.BooleanField(
        'campus status', default=False)
    account_activated = models.BooleanField(default=False)
    provinces = models.ManyToManyField(
        'ford3.Province',
        blank=True)
    creator = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.PROTECT)

    @classmethod
    def set_user_from_type(self, user):
        # model_class_name = user.type.split('_')[1]
        if user.is_province:
            return ProvinceUser.objects.get(pk=user.id)
        # elif user.is_campus:
        #     return CampusUser(user)

    def __str__(self):
        return self.email

class CampusUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_campus = True
        self.username = self.email
        super().save(*args, **kwargs)

        group = Group.objects.get(pk=OpenEduGroups.CAMPUS.value)
        group.user_set.add(self)
    
    @property
    def providers(self):
        return []


class ProviderUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_provider = True
        self.username = self.email
        super().save(*args, **kwargs)

        group = Group.objects.get(pk=OpenEduGroups.PROVIDER.value)
        group.user_set.add(self)

    @property
    def providers(self):
        return []


class ProvinceUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_province = True
        self.username = self.email
        super().save(*args, **kwargs)

        # Add the ProvinceUser into the PROVINCE group.
        group = Group.objects.get(pk=OpenEduGroups.PROVINCE.value)
        group.user_set.add(self)


    @property
    def providers(self):

        return chain.from_iterable([
            province.providers
            for province in self.provinces.all()])

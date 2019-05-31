from itertools import chain
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from ford3.models.provider import Provider
from ford3.enums.open_edu_groups import OpenEduGroups


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, null=True)
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

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    @classmethod
    def set_user_from_type(self, user):
        if user.is_province:
            return ProvinceUser.objects.get(pk=user.id)
        elif user.is_provider:
            return ProviderUser.objects.get(pk=user.id)
        elif user.is_campus:
            return CampusUser.objects.get(pk=user.id)
        else:
            return user

    @property
    def edu_group(self):
        if self.is_superuser or self.is_staff:
            return True

        return [
            group[0] for group in [
                (oeg, getattr(self, f'is_{oeg.name.lower()}'))
                for oeg in OpenEduGroups] if group[1]][0]

    @property
    def providers(self):
        return Provider.objects \
            .all() \
            .values('id', 'name', 'province__name', 'deleted') \
            .annotate(number_of_campus=Count('campus'))

    @property
    def users(self):
        return User.objects.all()

    def __str__(self):
        return self.email


class CampusUser(User):
    class Meta:
        proxy = True

    @property
    def providers(self):
        return Provider.active_objects \
            .filter(created_by_id=self.creator_id) \
            .values('id', 'name', 'province__name') \
            .annotate(number_of_campus=Count('campus'))


class ProviderUser(User):
    class Meta:
        proxy = True

    @property
    def providers(self):
        return Provider.active_objects \
            .filter(created_by_id=self.id) \
            .values('id', 'name', 'province__name') \
            .annotate(number_of_campus=Count('campus'))

    @property
    def users(self):
        return User.objects.filter(
            is_campus=True,
            creator=self)


class ProvinceUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_province = True
        super().save(*args, **kwargs)


    @property
    def providers(self):
        return chain.from_iterable([
            province.providers
            for province in self.provinces.all()])

    @property
    def users(self):
        return User.objects.filter(
            is_provider=True,
            creator=self)

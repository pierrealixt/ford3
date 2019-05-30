from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model


class ActiveProviderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Province(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The name of the province",
        max_length=255)
    location = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The province's location",
        max_length=255)
    users = models.ManyToManyField(
        get_user_model(),
        blank=True)

    def __str__(self):
        return self.name

    @property
    def providers(self):
        queryset = self.provider_set \
            .all() \
            .filter(deleted=False) \
            .values('id', 'name', 'province__name') \
            .annotate(number_of_campus=Count('campus'))
        return list(queryset)

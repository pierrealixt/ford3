from django.db import models
from django.contrib.auth import get_user_model


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
        through=get_user_model().provinces.through,
        blank=True)

    def __str__(self):
        return self.name

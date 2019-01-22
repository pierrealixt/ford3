from django.db import models
from ford3.models.secondary_institution_type import SecondaryInstitutionType


class Subject(models.Model):
    secondary_institution_types = models.ManyToManyField(
        SecondaryInstitutionType)

    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='',
        primary_key=True)
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    description = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    def __str__(self):
        return self.name

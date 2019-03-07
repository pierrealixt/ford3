from django.db import models

from ford3.models.qualification import Qualification


class QualificationEvent(models.Model):
    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='Key of qualification event',
        primary_key=True)
    qualification_id = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    date_start = models.DateField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    date_end = models.DateField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    http_link = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)

    def __str__(self):
        return self.name

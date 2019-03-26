from django.db import models

from ford3.models.qualification import Qualification


class QualificationEvent(models.Model):
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=255)
    date_start = models.DateField(
        blank=True,
        null=True,
        help_text='')
    date_end = models.DateField(
        blank=True,
        null=True,
        help_text='')
    event_date = models.DateField(
        blank=True,
        null=True
    )
    other_event = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
    http_link = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=255)

    def __unicode__(self):
        return self.name

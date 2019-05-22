from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


class QualificationEvent(models.Model):
    qualification = models.ForeignKey(
        'Qualification',
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        help_text="A short identifier for the event",
        max_length=255)
    date_start = models.DateField(
        blank=False,
        null=False,
        help_text="When does this event start?")
    date_end = models.DateField(
        blank=False,
        null=False,
        help_text="When does this event end?")
    event_date = models.DateField(
        blank=True,
        null=True
    )
    other_event = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
    http_link = models.URLField(
        blank=True,
        null=True,
        unique=False,
        help_text=(
            "A link to a web page with additional details regarding this "
            "event"),
        max_length=255)

    def save(self, *args, **kwargs):
        if self.date_start > self.date_end:
            raise ValidationError(
                'The start date must be before the end date')
        if isinstance(self.date_end, str):
            self.date_end = datetime.strptime(
                self.date_end, '%Y-%m-%d').date()
        if self.date_end < datetime.now().date():
            raise ValidationError('The end date may not be in the past')
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

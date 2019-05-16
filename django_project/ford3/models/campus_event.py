from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


class CampusEvent(models.Model):

    campus = models.ForeignKey(
        'ford3.campus',
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The name of this event",
        max_length=255)
    date_start = models.DateField(
        blank=False,
        null=False,
        unique=False,
        help_text='The date on which the event starts')
    date_end = models.DateField(
        blank=False,
        null=False,
        unique=False,
        help_text='The date on which the event ends')
    http_link = models.URLField(
        blank=True,
        null=True,
        unique=False,
        help_text='A link to a web page containing additional details '
                  'regarding this event',
        max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.date_start > self.date_end:
            raise ValidationError('The start date must be before the end date')
        print(type(self.date_end))
        if isinstance(self.date_end, str):
            self.date_end = datetime.strptime(self.date_end, '%Y-%m-%d').date()
        if self.date_end < datetime.now().date():
            raise ValidationError('The start date may not be in the past')

        super().save(*args, **kwargs)


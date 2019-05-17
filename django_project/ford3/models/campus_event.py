from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


class ActiveCampusEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class CampusEvent(models.Model):
    objects = models.Manager()
    active_objects = ActiveCampusEventManager()

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

    deleted = models.BooleanField(
        default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.deleted:
            if self.date_start > self.date_end:
                raise ValidationError(
                    'The start date must be before the end date')
            if isinstance(self.date_end, str):
                self.date_end = datetime.strptime(
                    self.date_end, '%Y-%m-%d').date()
            if self.date_end < datetime.now().date():
                raise ValidationError('The end date may not be in the past')
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted = True
        self.save()

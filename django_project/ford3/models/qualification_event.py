from django.db import models



class QualificationEvent(models.Model):
    qualification = models.ForeignKey(
        'Qualification',
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

    def __str__(self):
        return self.name

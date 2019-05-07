from django.db import models


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
        blank=False,
        null=True,
        unique=False,
        help_text='A link to a web page containing additional details '
                  'regarding this event',
        max_length=255)

    def __str__(self):
        return self.name

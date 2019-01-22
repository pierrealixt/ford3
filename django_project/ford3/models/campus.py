from django.contrib.gis.db import models

from ford3.models.provider import Provider


class Campus(models.Model):
    provider_id = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE)

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
    # location = models.PointField(
    #   blank=True,
    #   null=True,
    #   help_text='The spatial point position of the campus')

    pass

    def __str__(self):
        return self.name



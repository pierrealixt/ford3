from django.contrib.gis.db import models

from ford3.models.provider import Provider
from ford3.models.address import Address


class Campus(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    location = models.PointField(
      blank=True,
      null=True,
      help_text='The spatial point position of the campus')
    photo = models.FileField(
        blank=False,
        null=True,
        help_text='Representative photo of campus',
        upload_to='campus/photo'
    )
    telephone = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    email = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    max_students_per_year = models.IntegerField(
        blank=False,
        null=True,
        unique=False,
        help_text='')
    physical_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='physical_address',
        blank=True,
        null=True)

    postal_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='postal_address',
        blank=True,
        null=True)

    pass

    def __str__(self):
        return self.name

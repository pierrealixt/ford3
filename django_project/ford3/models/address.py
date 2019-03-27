from django.contrib.gis.db import models


class Address(models.Model):

    street_name = models.CharField(
        blank=False,
        null=True,
        max_length=255
    )

    city = models.CharField(
        blank=False,
        null=True,
        max_length=255
    )

    zip_code = models.CharField(
        blank=False,
        null=True,
        max_length=255
    )

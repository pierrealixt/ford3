from django.db import models


class Provider(models.Model):
    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='',
        primary_key=True)
    name = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    website = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    logo_url = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    email = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    admissions_contact_no = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    postal_address = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)

    pass

    def __str__(self):
        return self.name


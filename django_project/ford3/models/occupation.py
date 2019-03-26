from django.db import models


class Occupation(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    description = models.TextField(
        blank=True,
        null=True,
        help_text='')
    green_occupation = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text='')
    scarce_skill = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text='')
    tasks = models.TextField(
        blank=True,
        null=True,
        help_text='')
    pass

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description

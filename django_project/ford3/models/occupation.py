from django.db import models


class Occupation(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    description = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=500)

    pass

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description

from django.db import models


class FieldOfStudy(models.Model):
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

    pass

    def __str__(self):
        return self.name

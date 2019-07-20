from django.db import models


class PeopleGroup(models.Model):
    group = models.CharField(
        blank=True,
        null=True,
        unique=True,
        help_text='A group of people.',
        max_length=255)


    def __str__(self):
        return self.group

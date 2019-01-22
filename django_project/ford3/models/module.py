from django.db import models


class Module(models.Model):
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
    description = models.CharField(
      blank=True,
      null=True,
      unique=False,
      help_text='',
      max_length=255)

    pass

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description

from django.db import models


class FosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name').exclude(
            name='Undefined')


class FieldOfStudy(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The field of study's name",
        max_length=255)

    objects = FosManager()

    def __str__(self):
        return self.name

from django.db import models


class FieldOfStudy(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The field of study's name",
        max_length=255)

    pass

    def __str__(self):
        return self.name

from django.db import models


class Interest(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="A short identifier for the interest",
        max_length=255)

    pass

    def __str__(self):
        return self.name

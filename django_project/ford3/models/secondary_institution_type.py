from django.db import models


class SecondaryInstitutionType(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The name of the secondary institution type",
        max_length=255)

    pass

    def __str__(self):
        return self.name

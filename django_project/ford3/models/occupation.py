from django.db import models


class Occupation(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The occupation's name",
        max_length=255)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="A short description of the occupation")
    green_occupation = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text="Is this an occupation suited as a good first job")
    scarce_skill = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text='Would this occupation be consider a scarce skill')
    tasks = models.TextField(
        blank=True,
        null=True,
        help_text='A short summary of tasks involved with this occupation')
    pass

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description

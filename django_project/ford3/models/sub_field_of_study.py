from django.db import models
from ford3.models.field_of_study import FieldOfStudy
from ford3.models.occupation import Occupation


class SubFieldOfStudy(models.Model):
    field_of_study = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.PROTECT)
    occupation_id = models.ManyToManyField(Occupation)

    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)

    pass

    def __str__(self):
        return self.name

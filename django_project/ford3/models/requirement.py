from django.db import models
from ford3.models.qualification import Qualification


class Requirement(models.Model):
    qualification_id = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE)

    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='',
        primary_key=True)
    description = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    assessment = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    interview = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    admission_point_score = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    min_qualification = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')

    def __str__(self):
        return self.description

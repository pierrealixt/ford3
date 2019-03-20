from django.db import models
from ford3.models.qualification import Qualification
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel

class Requirement(models.Model):
    qualification_id = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE)

    id = models.AutoField(
        blank=False,
        null=False,
        unique=True,
        help_text='',
        primary_key=True)
    description = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=255)
    assessment = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    interview = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    admission_point_score = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    min_nqf_level = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=120,
        choices=[(level, level.value) for level in SaqaQualificationLevel]
    )
    portfolio = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    portfolio_comment = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=255)
    aps_calculator_link = models.URLField(
        blank=True,
        null=True,
        help_text='')

    def __str__(self):
        return self.description

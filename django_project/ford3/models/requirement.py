from django.db import models
from ford3.models.qualification import Qualification
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel


class Requirement(models.Model):
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE)

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
    require_aps_score = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    require_certain_subjects = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)

    def __unicode__(self):
        return self.description

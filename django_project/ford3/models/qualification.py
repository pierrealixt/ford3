from django.db import models
from ford3.models.campus import Campus
from ford3.models.module import Module
from ford3.models.occupation import Occupation
from ford3.models.sub_field_of_study import SubFieldOfStudy
from ford3.models.subject import Subject


class Qualification(models.Model):
    subjects = models.ManyToManyField(
        Subject,
        through='QualificationEntranceRequirementSubject')
    campus_id = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE)
    sub_field_of_study_id = models.ForeignKey(
        SubFieldOfStudy,
        on_delete=models.PROTECT)
    modules = models.ManyToManyField(Module)
    occupation_id = models.ForeignKey(
        Occupation,
        on_delete=models.PROTECT)

    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='Key of qualification',
        primary_key=True)
    qualification_id = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    saqa_id = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    short_description = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    long_description = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    nqf_level = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    duration_in_months = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    full_time = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    part_time = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    credits_after_completion = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    distance_learning = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    estimated_annual_fee = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')

    def __str__(self):
        return self.name

from django.db import models
from ford3.models.campus import Campus
from ford3.models.occupation import Occupation
from ford3.models.sub_field_of_study import SubFieldOfStudy
from ford3.models.subject import Subject
from ford3.models.interest import Interest


class Qualification(models.Model):
    subjects = models.ManyToManyField(
        Subject,
        through='QualificationEntranceRequirementSubject')
    campus_id = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE)
    sub_field_of_study_id = models.ForeignKey(
        SubFieldOfStudy,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    occupations = models.ManyToManyField(
        Occupation,
        null=True,
        blank=True)
    interests = models.ManyToManyField(
        Interest,
        null=True,
        blank=True)

    id = models.AutoField(
        blank=False,
        null=False,
        unique=True,
        help_text='Key of qualification',
        primary_key=True)
    saqa_id = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    short_description = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=120)
    long_description = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=500)
    nqf_level = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    duration_in_months = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    full_time = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')
    part_time = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')
    credits_after_completion = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    distance_learning = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')
    completion_rate = models.IntegerField(
        blank=True,
        null=True,
        help_text='',
        default=0)
    total_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='')
    total_cost_comment = models.CharField(
        blank=True,
        null=True,
        help_text='',
        max_length=255)
    critical_skill = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    green_occupation = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)
    high_demand_occupation = models.BooleanField(
        blank=True,
        null=True,
        help_text='',
        default=False)

    def __str__(self):
        return self.name

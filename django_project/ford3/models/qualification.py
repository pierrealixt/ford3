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
        on_delete=models.PROTECT)
    occupation_id = models.ForeignKey(
        Occupation,
        on_delete=models.PROTECT)
    interests = models.ManyToManyField(
        Interest)

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
    completion_rate = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        default=0)
    total_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=False,
        null=False,
        unique=False,
        help_text='')
    total_cost_comment = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    critical_skill = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        default=False)
    green_occupation = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        default=False)
    high_demand_occupation = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        default=False)



    def __str__(self):
        return self.name

from django.db import models
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.requirement import Requirement


class Qualification(models.Model):
    subjects = models.ManyToManyField(
        'ford3.subject',
        through='QualificationEntranceRequirementSubject')
    campus = models.ForeignKey(
        'ford3.campus',
        on_delete=models.CASCADE)
    saqa_qualification = models.ForeignKey(
        SAQAQualification,
        null=True,
        on_delete=models.PROTECT)
    occupations = models.ManyToManyField(
        'ford3.occupation',
        blank=True)
    interests = models.ManyToManyField(
        'ford3.interest',
        blank=True)
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
        return self.saqa_qualification.name

    @property
    def requirements(self):

        requirement_query = Requirement.objects.filter(
            qualification__id=self.id).order_by('id').values()
        return list(requirement_query)

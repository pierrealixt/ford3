from django.db import models
from typing import List
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.requirement import Requirement
from ford3.models.interest import Interest
from ford3.models.occupation import Occupation
from ford3.models.qualification_entrance_requirement_subject import \
    QualificationEntranceRequirementSubject
from ford3.models.qualification_event import QualificationEvent


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
    def requirements(self) -> List[Requirement]:
        requirement_query = Requirement.objects.filter(
            qualification__id=self.id).order_by('id').values()
        return list(requirement_query)

    @property
    def requirement(self) -> Requirement:
        requirement_query = Requirement.objects.filter(
            qualification__id=self.id).order_by('id').first()
        return requirement_query

    def add_events(self, qualification_events):
        if len(qualification_events) == 0:
            return
        for each_qualification_event in qualification_events:
            each_qualification_event.qualification = self
            each_qualification_event.save()

    @property
    def interest_id_list(self) -> List[int]:
        result = []
        interest_query = Interest.objects.filter(
            qualification__id=self.id).order_by('id').values('id')
        interest_query_list = list(interest_query)
        for each_item in interest_query_list:
            result.append(each_item['id'])
        return result

    @property
    def occupation_id_list(self) -> List[int]:
        result = []
        occupation_query = Occupation.objects.filter(
            qualification__id=self.id).order_by('id').values('id')
        occupation_query_list = list(occupation_query)
        for each_item in occupation_query_list:
            result.append(each_item['id'])
        return result

    @property
    def entrance_req_subjects_list(self):
        result = []
        subject_query = QualificationEntranceRequirementSubject.objects.filter(
            qualification__id=self.id)
        idx = 0
        for each_subject in subject_query:
            idx += 1
            next_subject = {}
            next_subject['index'] = idx
            next_subject['name'] = each_subject.subject.name
            next_subject['minimum_score'] = each_subject.minimum_score
            next_subject['id'] = each_subject.id
            result.append(next_subject)
        return result

    @property
    def qualification_events_list(self) -> List[QualificationEvent]:
        event_query = QualificationEvent.objects.filter(
            qualification__id=self.id).values()
        return list(event_query)

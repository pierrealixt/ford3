from typing import List
from django.db import models
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.requirement import Requirement
from ford3.models.interest import Interest
from ford3.models.occupation import Occupation
from ford3.models.qualification_entrance_requirement_subject import QualificationEntranceRequirementSubject  # noqa
from ford3.models.qualification_event import QualificationEvent
from ford3.models_logic.qualification_audit import QualificationAudit


class ActiveQualificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Qualification(models.Model):
    subjects = models.ManyToManyField(
        'ford3.subject',
        through='QualificationEntranceRequirementSubject')
    campus = models.ForeignKey(
        'ford3.campus',
        on_delete=models.CASCADE,
        related_name='qualification_set')
    saqa_qualification = models.ForeignKey(
        SAQAQualification,
        null=True,
        on_delete=models.PROTECT)
    published = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text="Has this qualification been published?")

    ready_to_publish = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text=("Has the qualification's details been completed in enough "
                   "detail to allow publication."))
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
        help_text="The qualification's name",
        max_length=255)
    short_description = models.CharField(
        blank=True,
        null=True,
        help_text="A short description of what the qualification entails",
        max_length=250)
    long_description = models.CharField(
        blank=True,
        null=True,
        help_text="A longer description of the qualification for the student"
                  " who is interested and would like to know more",
        max_length=500)
    duration = models.IntegerField(
        blank=True,
        null=True,
        help_text="How long the qualification takes to complete")
    duration_time_repr = models.CharField(
        blank=True,
        null=True,
        help_text="Represent the duration of the qualification in month or year", # noqa
        max_length=100
    )
    full_time = models.BooleanField(
        blank=True,
        null=True,
        help_text="Can this qualification be completed on a full-time basis?")
    credits_after_completion = models.IntegerField(
        blank=True,
        null=True,
        help_text="How many credits are awarded after completion?")
    distance_learning = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text="Does this qualification have a distance learning option?")
    completion_rate = models.IntegerField(
        blank=True,
        null=True,
        help_text="What has the completion rate for this qualifcation been?",
        default=0)
    total_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="What is the total cost to complete this qualification?")
    total_cost_comment = models.CharField(
        blank=True,
        null=True,
        help_text="Any comments regarding the cost and payment options of "
                  "this qualification should be filled in here",
        max_length=255)
    critical_skill = models.BooleanField(
        blank=True,
        null=True,
        help_text="Would the skill obtained by completing this qualification "
                  "be considered a critical skill?",
        default=False)
    green_occupation = models.BooleanField(
        blank=True,
        null=True,
        help_text="Would the occupations this qualification prepares you for "
                  "be considered environmentally friendly?",
        default=False)
    high_demand_occupation = models.BooleanField(
        blank=True,
        null=True,
        help_text="Are the occupations this qualification prepares you for "
                  "in high demand?",
        default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)
    edited_at = models.DateTimeField(
        auto_now=True)

    created_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='qualification_created_by'
    )

    edited_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='qualification_edited_by'
    )

    deleted = models.BooleanField(
        default=False,
        help_text="Qualification has been deleted")

    deleted_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='qualification_deleted_by'
    )

    objects = models.Manager()
    active_objects = ActiveQualificationManager()

    def __str__(self):
        return self.saqa_qualification.name

    def audit_for_publish(self):
        audit_result = QualificationAudit(self).evaluate_audit()

        if not self.published and audit_result and not self.ready_to_publish:
            self.ready_to_publish = True
            self.save()
        elif (self.ready_to_publish or self.published) and not audit_result:
            self.ready_to_publish = False
            self.published = False
            self.save()

    @property
    def requirement(self):
        try:
            return Requirement.objects.get(
                qualification_id=self.id)
        except Requirement.DoesNotExist:
            return None

    @property
    def interest_id_list(self) -> List[int]:
        interest_query = Interest.objects.filter(
            qualification__id=self.id).order_by('id').values('id')
        interest_query_list = list(interest_query)
        result = [each_item['id'] for each_item in interest_query_list]
        return result

    @property
    def interest_name_list(self) -> List[int]:
        interest_query = Interest.objects.filter(
            qualification__id=self.id).order_by('id').values('name')
        interest_query_list = list(interest_query)
        result = [each_item['name'] for each_item in interest_query_list]
        return result

    @property
    def occupation_ids(self) -> List[str]:
        return [
            str(i['id']) for i
            in list(self.occupations.all().values('id'))
        ]

    @property
    def occupation_name_list(self) -> List[int]:
        occupation_query = Occupation.objects.filter(
            qualification__id=self.id).order_by('id').values('name')
        occupation_query_list = list(occupation_query)
        result = [each_item['name'] for each_item in occupation_query_list]
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
    def events(self) -> List[QualificationEvent]:
        event_query = QualificationEvent.objects.filter(
            qualification__id=self.id).values()
        return list(event_query)

    @property
    def part_time(self):
        return not self.full_time

    def set_saqa_qualification(self, saqa_id):
        """
        Set SAQA qualificiation.
        """
        saqa_qualif = SAQAQualification.objects.get(id=saqa_id)
        self.saqa_qualification = saqa_qualif

    def toggle_occupations(self, occupations_ids):
        # save new occupations
        # symmetric difference
        ids = set(self.occupation_ids) ^ set(occupations_ids.split(' '))
        ids = [id for id in ids if len(id) > 0]
        for occupation_id in ids:
            occupation = Occupation.objects.get(pk=occupation_id)
            self.occupations.add(occupation)

        # remove occupations
        ids = set(occupations_ids.split(' ')) ^ set(self.occupation_ids)
        ids = [id for id in ids if len(id) > 0]
        for occupation_id in ids:
            occupation = Occupation.objects.get(pk=occupation_id)
            self.occupations.remove(occupation)

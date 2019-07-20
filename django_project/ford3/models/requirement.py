import re
from django.db import models
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel
from ford3.models.admission_point_score import AdmissionPointScore
from ford3.models.people_group import PeopleGroup


class Requirement(models.Model):
    qualification = models.ForeignKey(
        'ford3.qualification',
        on_delete=models.CASCADE,
        related_name='requirement_set')

    description = models.CharField(
        blank=True,
        null=True,
        help_text="A summary of the requirements and type of requirements "
                  "required for the assocaited qualification",
        max_length=255)
    assessment = models.BooleanField(
        blank=True,
        null=True,
        help_text="Is there an assessment as part of the application process?")
    assessment_comment = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='Additional information regarding the assessment involved.',
        max_length=255)

    interview = models.BooleanField(
        blank=True,
        null=True,
        help_text="Is there an interview as part of the application process?")

    min_nqf_level = models.CharField(
        blank=True,
        null=True,
        help_text="The minimum NQF level a person needs to have obtained to "
                  "apply for this qualification",
        max_length=120,
        choices=[(level, level.value) for level in SaqaQualificationLevel]
    )
    portfolio = models.BooleanField(
        blank=True,
        null=True,
        help_text="Does the applicant need to submit a portfolio as part of "
                  "the application process?")
    portfolio_comment = models.CharField(
        blank=True,
        null=True,
        help_text="Additional information regarding the portfolio to be "
                  "submitted",
        max_length=255)

    aps_calculator_link = models.URLField(
        blank=True,
        null=True,
        help_text="A link a calculator or the specifications for calculating"
                  " the required APS score.")
    require_aps_score = models.BooleanField(
        blank=True,
        null=True,
        help_text="Does the applicant need to acheive a certain APS score?")
    require_certain_subjects = models.BooleanField(
        blank=True,
        null=True,
        help_text="Are there specific subjects listed as a prerequisite for "
                  "this qualification")

    def __unicode__(self):
        return self.description

    @property
    def admission_point_scores(self):
        aps_set = AdmissionPointScore.objects.filter(requirement=self.id)
        result = []
        for pg in PeopleGroup.objects.all():
            try:
                aps = aps_set.get(people_group=pg.id)
            except AdmissionPointScore.DoesNotExist:
                from collections import namedtuple
                aps = namedtuple('aps', ['id', 'value'])
                aps = aps(*[0, 0])

            result.append({
                'id': aps.id,
                'value': aps.value,
                'group': {'id': pg.id, 'name': pg.group}
            })
        return result

    @admission_point_scores.setter
    def admission_point_scores(self, data):
        aps_set = AdmissionPointScore.objects.filter(requirement=self.id)
        for aps_tuple in data.split(','):
            match = re.match(r'\(([0-9]*) ([0-9]*)\)', aps_tuple)
            if match:
                people_group_id, value = match.groups()
                try:
                    aps = aps_set.get(people_group=people_group_id)
                    aps.value = value
                    aps.save()
                except AdmissionPointScore.DoesNotExist:
                    aps = AdmissionPointScore()
                    aps.people_group = PeopleGroup.objects.get(
                        pk=people_group_id)
                    aps.requirement = self
                    aps.value = value

                aps.save()

    def reset_admission_point_scores(self):
        AdmissionPointScore.objects.filter(requirement=self.id).delete()

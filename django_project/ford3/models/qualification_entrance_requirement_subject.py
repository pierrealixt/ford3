from django.db import models
from ford3.models.qualification import Qualification
from ford3.models.subject import Subject


class QualificationEntranceRequirementSubject(models.Model):
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.PROTECT)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT)

    minimum_score = models.IntegerField(
        blank=True,
        null=True,
        help_text='')
    required = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')

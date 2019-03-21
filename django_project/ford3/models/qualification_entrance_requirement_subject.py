from django.db import models
from ford3.models.qualification import Qualification
from ford3.models.subject import Subject


class QualificationEntranceRequirementSubject(models.Model):
    qualification_id = models.ForeignKey(
        Qualification,
        on_delete=models.PROTECT)
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT)

    minimum_score = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    required = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')
